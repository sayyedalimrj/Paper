"""
pipeline.py
===========
End-to-end orchestrator. Runs the full workflow and writes every artefact under
outputs/. Notebooks can import and call these functions, or run them as a script:

    python -m src.pipeline
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

try:
    from src import (config, utils, data_download, data_cleaning,
                     train_strength_model, explainability, train_carbon_model,
                     generate_passports, ifc_mapping)
except ImportError:
    import config, utils, data_download, data_cleaning, train_strength_model, \
        explainability, train_carbon_model, generate_passports, ifc_mapping  # type: ignore

LOG = utils.get_logger("pipeline")


def dataset_summary(df: pd.DataFrame) -> pd.DataFrame:
    desc = df.describe().T[["mean", "std", "min", "25%", "50%", "75%", "max"]].round(2)
    desc.insert(0, "n_non_null", df.notna().sum().values)
    desc = desc.reset_index().rename(columns={"index": "variable"})
    path = config.TABLES_DIR / "dataset_summary.csv"
    desc.to_csv(path, index=False)
    LOG.info("Saved dataset summary -> %s", path)
    return desc


def model_performance_summary(metrics: pd.DataFrame, best_name: str) -> pd.DataFrame:
    out = metrics.copy()
    out["is_best"] = out["model"] == best_name
    out = out.round(4)
    path = config.TABLES_DIR / "model_performance_summary.csv"
    out.to_csv(path, index=False)
    LOG.info("Saved model performance summary -> %s", path)
    return out


def limitations_table() -> pd.DataFrame:
    rows = [
        ("Strength dataset scope", "UCI dataset uses 8 mix-design inputs only (no cement chemistry, gradation, curing regime beyond age).", "Incorporate richer mix/curing/chemistry datasets; transfer learning."),
        ("Durability not modelled", "No clean, complete public durability dataset; durability left as schema extension.", "Integrate a vetted durability dataset (e.g., chloride/carbonation) when available."),
        ("Carbon estimate", "ICE per-constituent factors are generic cradle-to-gate; EPD benchmark is U.S.-centric.", "Use product/region-specific verified EPDs; expand to other regions."),
        ("BIM context illustrative", "Element IDs/types/required strengths/volumes are demonstration data, not a real model.", "Apply to a real IFC project model with project-specific requirements."),
        ("IFC/IDS specification-level", "Custom Pset + IDS are conceptual; not certified against commercial checkers.", "Author full IFC, validate IDS in BIMcollab/IfcOpenShell/IDS tooling."),
        ("Prediction uncertainty", "Uncertainty via ensemble spread/residual std; not calibrated intervals.", "Adopt conformal prediction or quantile models for calibrated bounds."),
        ("No causal claims", "Feature importance/SHAP are associational, not causal.", "Combine with mechanistic/physics-informed models."),
    ]
    df = pd.DataFrame(rows, columns=["limitation", "description", "future_work"])
    path = config.TABLES_DIR / "limitations_and_future_work.csv"
    df.to_csv(path, index=False)
    LOG.info("Saved limitations/future-work -> %s", path)
    return df


def framework_diagram() -> Path:
    """Scientific workflow:
    Raw data -> ML prediction -> uncertainty/risk/evidence -> passport
    -> OpenBIM/IDS requirements -> QA/QC & sustainability decision support.
    """
    config.ensure_dirs()
    fig, ax = plt.subplots(figsize=(14, 5.2))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis("off")

    stages = [
        ("Raw concrete data\n\nUCI strength (Yeh 1998)\nEPD GWP (Broyles 2024)\nICE factors", "#deebf7"),
        ("ML prediction\n\nRF / GBR / ExtraTrees\n(+XGBoost/LightGBM)\ncompressive strength", "#c6dbef"),
        ("Uncertainty / risk /\nevidence layer\n\nensemble spread (approx PI)\nrisk class + evidence A-D\nprovenance", "#c7e9c0"),
        ("Concrete Performance\nPassport\n\nBIM element + mix\nprediction + risk\ncarbon class + readiness", "#fee6ce"),
        ("OpenBIM / IDS\ninformation requirements\n\nIfcMaterial, Pset_MaterialConcrete\nPset_ConcretePerformancePassport\nIDS requirement matrix", "#fdd0a2"),
        ("QA/QC & sustainability\ndecision support\n\nAccept / Review /\nHold / Retest / Missing\n+ carbon class", "#e7d4e8"),
    ]
    n = len(stages)
    gap = 0.35
    w = (14 - (n + 1) * gap) / n
    h = 3.6
    y = 1.0
    centers = []
    for k, (label, color) in enumerate(stages):
        x = gap + k * (w + gap)
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.10",
                             linewidth=1.1, edgecolor="#555555", facecolor=color)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=7.6)
        centers.append((x, x + w))
    for k in range(n - 1):
        x0 = centers[k][1]; x1 = centers[k + 1][0]
        ax.add_patch(FancyArrowPatch((x0, y + h / 2), (x1, y + h / 2),
                                     arrowstyle="-|>", mutation_scale=16, linewidth=1.6, color="#333333"))
    ax.text(7, 5.5, "AI-Enabled Concrete Performance Passport — scientific workflow",
            ha="center", va="center", fontsize=12.5, fontweight="bold")
    ax.text(7, 0.45,
            "Evidence levels: A=measured, B=verified public/EPD, C=ML prediction, D=illustrative   |   "
            "vendor-neutral, machine-checkable (IDS)",
            ha="center", va="center", fontsize=8, style="italic", color="#444444")
    path = config.FIGURES_DIR / "framework_diagram.png"
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    LOG.info("Saved framework diagram -> %s", path)
    return path


def run_all() -> Dict:
    config.ensure_dirs(); utils.set_seed()
    LOG.info("=== Phase: data ===")
    data_download.download_concrete_strength()
    clean_path = data_cleaning.clean()
    df = pd.read_csv(clean_path)
    ds = dataset_summary(df)

    LOG.info("=== Phase: strength model ===")
    res = train_strength_model.train(clean_path)
    mps = model_performance_summary(res["metrics"], res["best_name"])

    LOG.info("=== Phase: explainability (permutation/impurity; SHAP skipped for speed) ===")
    X = df[res["features"]].astype(float)
    y = df[config.STRENGTH_TARGET].astype(float)
    imp, method = explainability.explain(res["best_model"], X, res["features"], y, use_shap=False)

    LOG.info("=== Phase: carbon ===")
    carbon_res = train_carbon_model.run()

    LOG.info("=== Phase: passports ===")
    pp = generate_passports.generate(n=30)

    LOG.info("=== Phase: OpenBIM/IDS mapping ===")
    mapping = ifc_mapping.build_mapping()

    LOG.info("=== Phase: figures/tables ===")
    framework_diagram()
    limitations_table()

    return {
        "dataset_summary": ds, "metrics": res["metrics"], "best_name": res["best_name"],
        "importance_method": method, "carbon_source": carbon_res["source_note"],
        "passports_csv": pp["csv"], "n_passports": pp["n"],
        "ifc_note": mapping["ifc_note"],
    }


if __name__ == "__main__":
    summary = run_all()
    print("\n=== PIPELINE COMPLETE ===")
    print("Best strength model:", summary["best_name"])
    print("Explainability method:", summary["importance_method"])
    print("Carbon source:", summary["carbon_source"])
    print("Passports:", summary["n_passports"], "->", summary["passports_csv"])
    print("IFC note:", summary["ifc_note"])
