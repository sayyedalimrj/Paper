"""
explainability.py  (Phase 2 — implemented)
===========================================
Model explanations for the strength model.

Strategy (with graceful fallback):
  1. SHAP TreeExplainer on a small sample (fast, exact for tree ensembles).
  2. If SHAP is unavailable/slow/fails -> sklearn permutation importance.
  3. If that fails -> built-in impurity importance.

Outputs:
  * outputs/figures/strength_explainability.png
  * outputs/tables/strength_feature_importance_values.csv
Returns a tidy importance DataFrame and the method actually used.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from src import config, utils
except ImportError:
    import config, utils  # type: ignore

LOG = utils.get_logger("explainability")


def explain(model, X: pd.DataFrame, feats: List[str],
            y: pd.Series | None = None, sample: int = 200,
            use_shap: bool = True) -> Tuple[pd.DataFrame, str]:
    """Compute and plot feature importance; return (importance_df, method).

    If use_shap is False, SHAP is skipped entirely (faster, deterministic) and
    permutation importance (then impurity importance) is used instead.
    """
    config.ensure_dirs()
    Xs = X.sample(min(sample, len(X)), random_state=config.RANDOM_SEED)
    method = "none"
    importance = None

    # 1) SHAP (optional)
    if use_shap:
        try:
            import shap

            explainer = shap.TreeExplainer(model)
            sv = explainer.shap_values(Xs)
            importance = np.abs(sv).mean(axis=0)
            method = "SHAP (mean |value|)"
            _plot_shap(sv, Xs, feats)
            LOG.info("SHAP explanation succeeded.")
        except Exception as e:  # noqa: BLE001
            LOG.warning("SHAP unavailable/failed (%s); falling back.", type(e).__name__)
    else:
        LOG.info("use_shap=False -> using permutation/impurity importance.")

    # 2) Permutation importance
    if importance is None and y is not None:
        try:
            from sklearn.inspection import permutation_importance

            yc = y.loc[Xs.index]
            r = permutation_importance(
                model, Xs, yc, n_repeats=10, random_state=config.RANDOM_SEED, n_jobs=-1
            )
            importance = r.importances_mean
            method = "Permutation importance"
            LOG.info("Permutation importance succeeded.")
        except Exception as e:  # noqa: BLE001
            LOG.warning("Permutation importance failed (%s).", type(e).__name__)

    # 3) Impurity importance
    if importance is None:
        importance = getattr(model, "feature_importances_", np.ones(len(feats)) / len(feats))
        method = "Impurity-based importance"

    imp_df = (pd.DataFrame({"feature": feats, "importance": np.asarray(importance, float)})
              .sort_values("importance", ascending=False).reset_index(drop=True))
    imp_df["method"] = method
    imp_df.to_csv(config.TABLES_DIR / "strength_feature_importance_values.csv", index=False)

    # If SHAP didn't produce its own beeswarm, draw a bar chart as the explainability figure.
    fig_path = config.FIGURES_DIR / "strength_explainability.png"
    if not fig_path.exists() or not method.startswith("SHAP"):
        _plot_bar(imp_df, method, fig_path)
    LOG.info("Explainability method used: %s", method)
    return imp_df, method


def _plot_shap(sv, Xs, feats) -> None:
    import shap

    fig = plt.figure()
    shap.summary_plot(sv, Xs, feature_names=feats, show=False, plot_size=(8, 5))
    plt.title("SHAP summary — compressive strength model")
    plt.tight_layout()
    plt.savefig(config.FIGURES_DIR / "strength_explainability.png", dpi=150, bbox_inches="tight")
    plt.close("all")


def _plot_bar(imp_df: pd.DataFrame, method: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(imp_df["feature"], imp_df["importance"], color="#756bb1")
    ax.invert_yaxis(); ax.set_xlabel(method)
    ax.set_title(f"Feature importance — {method}")
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    import joblib

    art = joblib.load(config.MODELS_DIR / "best_strength_model.pkl")
    df = pd.read_csv(config.PROCESSED_DIR / "concrete_strength_clean.csv")
    X = df[art["features"]].astype(float)
    y = df[config.STRENGTH_TARGET].astype(float)
    out, method = explain(art["model"], X, art["features"], y)
    print("Method:", method)
    print(out.to_string(index=False))
