"""
finalize_lightweight_outputs.py
================================
The ONLY regeneration script for the scientific-hardening pass.

Design constraints (deliberate, to avoid the hang that affected the full
pipeline in this environment):
  * Uses LOCAL/CACHED data only — never downloads (sets USE_CACHED_ONLY=1).
  * No SHAP.
  * No cross-validation.
  * Lightweight models only (<=50 trees), single train/test split.
  * Targets completion in well under 2 minutes.
  * Never imports/calls src.pipeline's run_all.

It regenerates: strength model + metrics + figures, the Concrete Performance
Passport (CSV/JSON with all scientific fields), carbon benchmark + figure,
durability availability, OpenBIM mapping, IDS matrix, framework diagram,
risk-class figure, and the limitations table.
"""
from __future__ import annotations

import os
os.environ.setdefault("USE_CACHED_ONLY", "1")  # hard offline guarantee

from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

try:
    from src import (config, utils, data_cleaning, passport_schema as ps,
                     train_carbon_model as carbon, generate_passports, ifc_mapping)
    from src import train_strength_model as tsm
    from src import pipeline as pl
except ImportError:  # pragma: no cover
    import config, utils, data_cleaning, passport_schema as ps  # type: ignore
    import train_carbon_model as carbon, generate_passports, ifc_mapping  # type: ignore
    import train_strength_model as tsm  # type: ignore
    import pipeline as pl  # type: ignore

LOG = utils.get_logger("finalize")

TINY_FIXTURE_NOTE = "TINY FIXTURE (structural only) — real model results unavailable"


def _load_clean_data() -> tuple[pd.DataFrame, bool]:
    """Load processed clean CSV; else clean raw cache; else tiny fixture."""
    proc = config.PROCESSED_DIR / "concrete_strength_clean.csv"
    if proc.exists():
        return pd.read_csv(proc), True
    raw = config.RAW_DIR / "concrete_strength_raw.csv"
    if raw.exists():
        LOG.info("Processed missing; cleaning cached raw CSV locally (no download).")
        data_cleaning.clean(raw)
        return pd.read_csv(proc), True
    LOG.warning("No cached strength data; using tiny fixture (results unavailable).")
    rng = np.random.default_rng(config.RANDOM_SEED)
    n = 60
    df = pd.DataFrame({
        "cement": rng.uniform(150, 540, n), "blast_furnace_slag": rng.uniform(0, 200, n),
        "fly_ash": rng.uniform(0, 150, n), "water": rng.uniform(140, 220, n),
        "superplasticizer": rng.uniform(0, 12, n), "coarse_aggregate": rng.uniform(800, 1100, n),
        "fine_aggregate": rng.uniform(600, 900, n), "age": rng.choice([7, 28, 56], n),
    })
    df["compressive_strength"] = (0.09 * df["cement"] - 0.1 * df["water"]
                                  + 0.05 * df["age"] + rng.normal(20, 4, n)).clip(5, 80)
    df = data_cleaning.engineer_features(df)
    return df, False


def run_strength(df: pd.DataFrame, real_data: bool) -> Dict:
    feats = list(config.STRENGTH_FEATURES)
    X = df[feats].astype(float); y = df[config.STRENGTH_TARGET].astype(float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=config.TEST_SIZE,
                                          random_state=config.RANDOM_SEED)
    seed = config.RANDOM_SEED
    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=50, random_state=seed, n_jobs=-1),
        "ExtraTrees": ExtraTreesRegressor(n_estimators=50, random_state=seed, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(random_state=seed),
    }
    rows, fitted = [], {}
    for name, m in models.items():
        m.fit(Xtr, ytr)
        met = utils.regression_metrics(yte, m.predict(Xte))
        rows.append({"model": name, "r2": met["r2"], "rmse": met["rmse"],
                     "mae": met["mae"], "mape": met["mape"],
                     "cv_r2_mean": float("nan"), "cv_r2_std": float("nan"),
                     "note": "single split, no CV" + ("" if real_data else " | " + TINY_FIXTURE_NOTE)})
        fitted[name] = m
        LOG.info("%-16s R2=%.3f RMSE=%.2f", name, met["r2"], met["rmse"])

    metrics = pd.DataFrame(rows).sort_values("r2", ascending=False).reset_index(drop=True)
    metrics.to_csv(config.TABLES_DIR / "strength_model_metrics.csv", index=False)

    best_name = metrics.iloc[0]["model"]
    best_model = fitted[best_name]
    resid_std = float(np.std(yte.values - best_model.predict(Xte)))
    unc_model = fitted["RandomForest"]

    artefact = {
        "model": best_model, "model_name": best_name, "uncertainty_model": unc_model,
        "uncertainty_method": "Random Forest ensemble spread (std across 50 trees); approximate, not calibrated",
        "features": feats, "residual_std": resid_std, "target": config.STRENGTH_TARGET,
        "trained_utc": utils.utc_timestamp(), "n_train": int(len(Xtr)), "n_test": int(len(Xte)),
        "real_data": bool(real_data),
    }
    joblib.dump(artefact, config.MODELS_DIR / "best_strength_model.pkl")

    # figures (reuse train_strength_model helpers)
    tsm._plot_comparison(metrics, config.FIGURES_DIR / "strength_model_comparison.png")
    tsm._plot_feature_importance(best_model, feats, best_name,
                                 config.FIGURES_DIR / "strength_feature_importance.png")

    # impurity importance values + explainability figure (no SHAP, no permutation)
    imp = getattr(best_model, "feature_importances_", None)
    if imp is None:
        imp = np.abs(getattr(best_model, "coef_", np.ones(len(feats))))
        imp = imp / imp.sum() if imp.sum() else imp
    imp_df = (pd.DataFrame({"feature": feats, "importance": np.asarray(imp, float)})
              .sort_values("importance", ascending=False).reset_index(drop=True))
    imp_df["method"] = "Impurity-based importance (lightweight; SHAP skipped)"
    imp_df.to_csv(config.TABLES_DIR / "strength_feature_importance_values.csv", index=False)
    _plot_importance(imp_df, config.FIGURES_DIR / "strength_explainability.png")

    # model performance summary (reuse pipeline helper)
    pl.model_performance_summary(metrics, best_name)
    return {"metrics": metrics, "best_name": best_name}


def _plot_importance(imp_df: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(imp_df["feature"], imp_df["importance"], color="#756bb1")
    ax.invert_yaxis(); ax.set_xlabel("Impurity-based importance")
    ax.set_title("Feature importance (lightweight; SHAP skipped)")
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)


def run_carbon() -> str:
    """Cached EPD only -> benchmark summary + figure. Synthetic fallback if missing."""
    carbon.write_ice_factors()
    df, note = carbon.load_epd()  # respects USE_CACHED_ONLY; reads cache or synthetic
    # Efficiency: cap rows for figure/summary if very large.
    if len(df) > 20000:
        df_fig = df.sample(20000, random_state=config.RANDOM_SEED)
    else:
        df_fig = df
    carbon.build_benchmarks(df)          # full data for robust quartiles (small table)
    carbon.plot_distribution(df_fig)
    return note


def durability_availability() -> pd.DataFrame:
    rows = [{
        "durability_target": "chloride/​carbonation/​shrinkage/​creep",
        "status": "future extension / not modeled in this demonstration",
        "reason": "No clean, complete public durability dataset cached locally in this pass.",
        "schema_support": "durability_indicator_status field present in passport schema",
        "reference": "RILEM TC 315-DCS (2025) notes durability-data scarcity/heterogeneity.",
    }]
    df = pd.DataFrame(rows)
    df.to_csv(config.TABLES_DIR / "durability_data_availability.csv", index=False)
    LOG.info("Saved durability availability -> outputs/tables/durability_data_availability.csv")
    return df


def main() -> Dict:
    config.ensure_dirs(); utils.set_seed()
    LOG.info("USE_CACHED_ONLY=%s (offline)", os.environ.get("USE_CACHED_ONLY"))

    df, real = _load_clean_data()
    pl.dataset_summary(df)
    s = run_strength(df, real)

    carbon_note = run_carbon()
    pp = generate_passports.generate(n=30)   # uses saved model + cached EPD

    ifc_mapping.build_mapping()
    pl.framework_diagram()
    pl.limitations_table()
    durability_availability()

    LOG.info("=== FINALIZE COMPLETE ===")
    return {"best_name": s["best_name"], "carbon": carbon_note,
            "n_passports": pp["n"], "real_data": real}


if __name__ == "__main__":
    out = main()
    print("Best model:", out["best_name"], "| real_data:", out["real_data"])
    print("Carbon source:", out["carbon"])
    print("Passports:", out["n_passports"])
