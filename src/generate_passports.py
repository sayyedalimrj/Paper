"""
generate_passports.py  (scientific hardening)
=============================================
Builds Concrete Performance Passports by combining:
  * dataset-derived mix & test data (UCI),
  * model-derived predicted strength + approximate prediction interval
    (Random Forest ensemble spread) + risk class,
  * importance/SHAP-derived global top features,
  * ICE-estimated GWP + EPD-benchmarked carbon class/percentile,
  * a rule-based QA/QC decision + readiness/IDS-readiness scoring,
  * an evidence/provenance layer (A-D) and DPP/CPR relevance note,
  * deterministic, clearly-LABELLED illustrative BIM element context.

Outputs:
  * outputs/tables/concrete_performance_passports.csv
  * outputs/tables/concrete_performance_passports.json
  * outputs/figures/risk_class_distribution.png
  * outputs/passports/<element_id>.json
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from src import config, utils, passport_schema as ps, train_carbon_model as carbon
except ImportError:
    import config, utils, passport_schema as ps, train_carbon_model as carbon  # type: ignore

import joblib

LOG = utils.get_logger("generate_passports")

REQUIRED_STRENGTH_MPA = {
    "footing": 25.0, "slab": 30.0, "wall": 30.0, "beam": 32.0,
    "bridge_deck": 35.0, "pile": 35.0, "column": 40.0, "pier": 40.0,
}
VOLUME_RANGE = {
    "footing": (4, 20), "slab": (8, 40), "wall": (3, 15), "beam": (1, 6),
    "bridge_deck": (20, 80), "pile": (2, 12), "column": (1, 5), "pier": (10, 40),
}
EN206 = [(25, "C25/30"), (30, "C30/37"), (32, "C32/40"), (35, "C35/45"), (40, "C40/50")]

DATA_SOURCE_REFERENCE = (
    "Mix & measured strength: UCI Concrete dataset (Yeh, 1998); "
    "prediction: ML model on public data; carbon benchmark: compiled U.S. EPD "
    "dataset (Broyles, Gevaudan & Brown, 2024); carbon factors: ICE (Hammond & "
    "Jones, 2008); BIM element context: illustrative demonstration."
)
AUDIT_NOTE = (
    "Mixed evidence: measured strength = level B (public dataset); predicted "
    "strength = level C (ML from public data); carbon class = level B "
    "(EPD-benchmarked); element ID/type/required strength/volume = level D "
    "(illustrative). Decision basis = predicted strength (level C)."
)


def _material_class(req_mpa: float) -> str:
    for thr, label in EN206:
        if req_mpa <= thr:
            return label
    return "C45/55"


def _per_sample_std(artefact: Dict, X: pd.DataFrame) -> Optional[np.ndarray]:
    """Per-sample std across trees of the dedicated uncertainty RF (approximate)."""
    unc = artefact.get("uncertainty_model")
    if unc is not None and hasattr(unc, "estimators_"):
        try:
            preds = np.stack([t.predict(X.values) for t in unc.estimators_])
            return preds.std(axis=0)
        except Exception as e:  # noqa: BLE001
            LOG.warning("Per-sample std failed (%s); using global residual std.", e)
    return None


def _uncertainty_band(rel_unc: Optional[float]) -> str:
    if rel_unc is None:
        return "Unknown"
    if rel_unc < 0.07:
        return "Low"
    if rel_unc < 0.15:
        return "Medium"
    return "High"


def generate(n: int = 30) -> Dict:
    config.ensure_dirs(); utils.set_seed()

    artefact = joblib.load(config.MODELS_DIR / "best_strength_model.pkl")
    model, feats, residual_std = artefact["model"], artefact["features"], artefact["residual_std"]
    model_name = artefact["model_name"]
    unc_method = artefact.get("uncertainty_method", "Random Forest ensemble spread (approximate)")

    df = pd.read_csv(config.PROCESSED_DIR / "concrete_strength_clean.csv")
    sample = df.sample(n=min(n, len(df)), random_state=config.RANDOM_SEED).reset_index(drop=True)

    top_features = _top_features(model, feats)

    epd_df, epd_note = carbon.load_epd()
    carbon_summary = carbon.build_benchmarks(epd_df)

    X = sample[feats].astype(float)
    preds = model.predict(X)
    psstd = _per_sample_std(artefact, X)

    passports: List[ps.Passport] = []
    element_types = ps.ELEMENT_TYPES
    rng = np.random.default_rng(config.RANDOM_SEED)

    for i, row in sample.iterrows():
        etype = element_types[i % len(element_types)]
        req = REQUIRED_STRENGTH_MPA[etype]
        lo, hi = VOLUME_RANGE[etype]
        volume = round(float(rng.uniform(lo, hi)), 1)
        pred = float(preds[i])
        unc = float(psstd[i]) if psstd is not None else float(residual_std)
        rel_unc = float(unc / pred) if pred > 0 else None
        pi_lo = pred - 1.96 * unc
        pi_hi = pred + 1.96 * unc

        mix = {k: float(row.get(k, 0.0)) for k in carbon.ICE_FACTORS}
        gwp = carbon.estimate_gwp_from_mix(mix)
        strength_psi = pred * carbon.PSI_PER_MPA
        c_class, c_pct, c_group = carbon.classify_carbon(gwp, strength_psi, epd_df, carbon_summary)

        qa = ps.classify_qa(req, pred, rel_unc)
        risk = ps.classify_risk(req, pred, rel_unc)
        rationale = (f"Predicted {pred:.1f} MPa vs required {req:.1f} MPa "
                     f"(margin {((pred-req)/req*100):+.1f}%); approx. 95% PI "
                     f"[{pi_lo:.1f}, {pi_hi:.1f}] MPa; uncertainty band={_uncertainty_band(rel_unc)}.")

        key_fields = {
            "material_class": _material_class(req), "required_strength_mpa": req,
            "predicted_strength_mpa": pred, "risk_class": risk, "qa_qc_decision": qa,
            "prediction_uncertainty_mpa": unc, "carbon_class": c_class,
            "gwp_estimate_kgco2e_per_m3": gwp, "model_name": model_name, "volume_m3": volume,
        }
        readiness = ps.compute_readiness(key_fields)
        ids_status = ps.ids_readiness(key_fields)
        dsl = ps.decision_support_level(pred, c_class)

        p = ps.Passport(
            bim_element=ps.BIMElement(
                element_id=f"EL-{etype[:3].upper()}-{i+1:03d}",
                element_type=etype, required_strength_mpa=req,
                material_class=_material_class(req), volume_m3=volume,
                ifc_element_type=ps.ELEMENT_IFC_TYPE[etype]),
            mix_and_test=ps.MixAndTest(
                cement=float(row["cement"]), water=float(row["water"]),
                blast_furnace_slag=float(row["blast_furnace_slag"]),
                fly_ash=float(row["fly_ash"]), silica_fume=None,
                coarse_aggregate=float(row["coarse_aggregate"]),
                fine_aggregate=float(row["fine_aggregate"]),
                superplasticizer=float(row["superplasticizer"]),
                age_days=float(row["age"]),
                water_binder_ratio=(float(row["water_binder_ratio"])
                                    if "water_binder_ratio" in row and pd.notna(row["water_binder_ratio"]) else None),
                measured_strength_mpa=float(row[config.STRENGTH_TARGET])),
            ml_outputs=ps.MLOutputs(
                predicted_strength_mpa=pred, prediction_uncertainty_mpa=unc,
                relative_uncertainty=rel_unc if rel_unc is not None else float("nan"),
                model_confidence_or_uncertainty=_uncertainty_band(rel_unc),
                prediction_interval_lower=pi_lo, prediction_interval_upper=pi_hi,
                uncertainty_method=unc_method, risk_class=risk,
                risk_decision_rule=ps.RISK_DECISION_RULE,
                top_features=top_features, model_name=model_name),
            sustainability=ps.Sustainability(
                gwp_estimate_kgco2e_per_m3=gwp, carbon_class=c_class,
                carbon_benchmark_group=c_group, epd_benchmark_percentile=c_pct,
                durability_indicator_status="future extension"),
            decision=ps.DecisionReadiness(
                qa_qc_decision=qa, passport_readiness_score=readiness,
                ids_readiness_status=ids_status, decision_support_level=dsl,
                rationale=rationale),
            evidence=ps.Evidence(
                data_source_type="predicted",
                data_source_reference=DATA_SOURCE_REFERENCE,
                evidence_level="C",
                evidence_level_meaning=ps.EVIDENCE_LEVEL_MEANING["C"],
                auditability_note=AUDIT_NOTE),
            openbim_refs=ps.OpenBIMRefs(ids_requirement_ids=["IDS-CPP-01", "IDS-CPP-02",
                                                             "IDS-CPP-04", "IDS-CPP-05", "IDS-CPP-06"]),
        )
        passports.append(p)

    rows = [p.to_flat_row() for p in passports]

    # Explicit Missing Data demonstration (required strength absent).
    demo_missing = dict(rows[0])
    demo_missing.update({
        "element_id": "EL-DEMO-MISSING", "required_strength_mpa": None,
        "risk_class": "Unknown", "qa_qc_decision": "Missing Data",
        "decision_support_level": "descriptive",
        "evidence_level": "D", "evidence_level_meaning": ps.EVIDENCE_LEVEL_MEANING["D"],
        "data_source_type": "missing",
        "qa_rationale": "Required strength not provided -> insufficient information for a decision.",
        "auditability_note": "Demonstration of the Missing Data state (level D).",
    })
    # Recompute readiness/IDS for the missing record.
    demo_missing["passport_readiness_score"] = ps.compute_readiness(
        {**demo_missing, "required_strength_mpa": None})
    demo_missing["ids_readiness_status"] = ps.ids_readiness(
        {**demo_missing, "required_strength_mpa": None})
    rows.append(demo_missing)

    table = pd.DataFrame(rows)
    csv_path = config.TABLES_DIR / "concrete_performance_passports.csv"
    table.to_csv(csv_path, index=False)

    json_path = config.TABLES_DIR / "concrete_performance_passports.json"
    full = {
        "schema_version": "2.0",
        "disclaimer": ("BIM element context (IDs, types, required strengths, volumes) is "
                       "ILLUSTRATIVE demonstration data (evidence level D). Mix & measured "
                       "strength are dataset-derived (UCI, Yeh 1998; level B). Predicted "
                       "strength/uncertainty are model-derived (level C). Carbon class uses "
                       "ICE factors + public EPD benchmark (level B). No legal/regulatory "
                       "compliance is claimed; Pset_ConcretePerformancePassport is a PROPOSED "
                       "(non-official) IFC property set."),
        "uncertainty_method": unc_method,
        "epd_source": epd_note,
        "evidence_levels": ps.EVIDENCE_LEVEL_MEANING,
        "json_schema": ps.json_schema(),
        "passports": [p.to_dict() for p in passports],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full, f, indent=2, default=utils._json_default)

    for p in passports:
        utils.save_json(p.to_dict(), config.PASSPORTS_DIR / f"{p.bim_element.element_id}.json")

    _plot_risk(table, config.FIGURES_DIR / "risk_class_distribution.png")
    LOG.info("Generated %d passports (+1 missing-data demo) -> %s", len(passports), csv_path)
    return {"table": table, "csv": csv_path, "json": json_path, "n": len(passports),
            "epd_note": epd_note}


def _top_features(model, feats: List[str], k: int = 3) -> List[str]:
    path = config.TABLES_DIR / "strength_feature_importance_values.csv"
    if path.exists():
        try:
            d = pd.read_csv(path)
            return d.sort_values("importance", ascending=False)["feature"].head(k).tolist()
        except Exception:  # noqa: BLE001
            pass
    imp = getattr(model, "feature_importances_", None)
    if imp is not None:
        order = np.argsort(imp)[::-1][:k]
        return [feats[i] for i in order]
    return feats[:k]


def _plot_risk(table: pd.DataFrame, path: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    rc = table["risk_class"].value_counts()
    order_r = [c for c in ["Low", "Medium", "High", "Unknown"] if c in rc.index]
    rc_colors = {"Low": "#31a354", "Medium": "#fec44f", "High": "#de2d26", "Unknown": "#969696"}
    ax1.bar(order_r, [rc[c] for c in order_r], color=[rc_colors[c] for c in order_r])
    ax1.set_ylabel("count"); ax1.set_title("Risk-class distribution")
    qc = table["qa_qc_decision"].value_counts()
    order_q = [c for c in ps.QA_DECISIONS if c in qc.index]
    ax2.bar(order_q, [qc[c] for c in order_q], color="#3182bd")
    ax2.set_ylabel("count"); ax2.set_title("QA/QC decision distribution")
    plt.setp(ax2.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    LOG.info("Saved figure -> %s", path)


if __name__ == "__main__":
    out = generate()
    print(out["table"].head(8).to_string(index=False))
