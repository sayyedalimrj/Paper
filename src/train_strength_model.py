"""
train_strength_model.py  (Phase 2 — implemented)
=================================================
Train and compare compressive-strength regressors on the cleaned UCI dataset.

Models (always available via scikit-learn):
  * Linear Regression (interpretable baseline)
  * Random Forest Regressor
  * Gradient Boosting Regressor
  * Extra Trees Regressor
Optional (used only if importable): XGBoost, LightGBM, CatBoost.

Outputs:
  * outputs/tables/strength_model_metrics.csv
  * outputs/models/best_strength_model.pkl   (dict: model + metadata)
  * outputs/figures/strength_model_comparison.png
  * outputs/figures/strength_feature_importance.png

The saved artefact bundles the fitted model, the feature list, the residual
standard deviation (for a global uncertainty fallback), and the model kind, so
`generate_passports` can produce predictions *and* an uncertainty estimate.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, KFold

try:
    from src import config, utils, data_cleaning
except ImportError:  # script execution from within src/
    import config, utils, data_cleaning  # type: ignore

import joblib

LOG = utils.get_logger("train_strength_model")


def _optional_models() -> Dict[str, object]:
    """Return optional gradient-boosting models if their libraries import."""
    extra = {}
    try:
        from xgboost import XGBRegressor

        extra["XGBoost"] = XGBRegressor(
            n_estimators=400, max_depth=4, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9, random_state=config.RANDOM_SEED,
            n_jobs=-1, verbosity=0,
        )
    except Exception as e:  # noqa: BLE001
        LOG.info("XGBoost not available (%s) — skipping.", type(e).__name__)
    try:
        from lightgbm import LGBMRegressor

        extra["LightGBM"] = LGBMRegressor(
            n_estimators=500, max_depth=-1, learning_rate=0.05,
            subsample=0.9, random_state=config.RANDOM_SEED, n_jobs=-1, verbose=-1,
        )
    except Exception as e:  # noqa: BLE001
        LOG.info("LightGBM not available (%s) — skipping.", type(e).__name__)
    try:
        from catboost import CatBoostRegressor

        extra["CatBoost"] = CatBoostRegressor(
            iterations=500, depth=6, learning_rate=0.05,
            random_seed=config.RANDOM_SEED, verbose=False,
        )
    except Exception as e:  # noqa: BLE001
        LOG.info("CatBoost not available (%s) — skipping.", type(e).__name__)
    return extra


def build_models() -> Dict[str, object]:
    seed = config.RANDOM_SEED
    models: Dict[str, object] = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(
            n_estimators=200, random_state=seed, n_jobs=-1
        ),
        "GradientBoosting": GradientBoostingRegressor(random_state=seed),
        "ExtraTrees": ExtraTreesRegressor(
            n_estimators=200, random_state=seed, n_jobs=-1
        ),
    }
    models.update(_optional_models())
    return models


def load_features(processed_csv: Path | None = None) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """Load cleaned data; return X (8 canonical mix features), y, feature names."""
    processed_csv = Path(processed_csv) if processed_csv else config.PROCESSED_DIR / "concrete_strength_clean.csv"
    if not processed_csv.exists():
        LOG.info("Cleaned CSV missing; running data_cleaning.clean() ...")
        data_cleaning.clean()
    df = pd.read_csv(processed_csv)
    feats = list(config.STRENGTH_FEATURES)  # 8 canonical mix-design inputs
    X = df[feats].astype(float)
    y = df[config.STRENGTH_TARGET].astype(float)
    return X, y, feats


def train(processed_csv: Path | None = None) -> Dict:
    """Train/compare models, evaluate, save artefacts, return a summary dict."""
    config.ensure_dirs()
    utils.set_seed()
    X, y, feats = load_features(processed_csv)
    LOG.info("Training on %d rows, %d features.", len(X), len(feats))

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_SEED
    )
    cv = KFold(n_splits=config.CV_FOLDS, shuffle=True, random_state=config.RANDOM_SEED)

    rows = []
    fitted = {}
    for name, model in build_models().items():
        try:
            model.fit(X_tr, y_tr)
            pred = model.predict(X_te)
            m = utils.regression_metrics(y_te, pred)
            try:
                cv_r2 = cross_val_score(model, X, y, cv=cv, scoring="r2", n_jobs=-1)
                cv_mean, cv_std = float(cv_r2.mean()), float(cv_r2.std())
            except Exception as e:  # noqa: BLE001
                LOG.warning("CV failed for %s: %s", name, e)
                cv_mean, cv_std = float("nan"), float("nan")
            rows.append({
                "model": name, "r2": m["r2"], "rmse": m["rmse"],
                "mae": m["mae"], "mape": m["mape"],
                "cv_r2_mean": cv_mean, "cv_r2_std": cv_std,
            })
            fitted[name] = model
            LOG.info("%-16s R2=%.3f RMSE=%.2f MAE=%.2f CV_R2=%.3f",
                     name, m["r2"], m["rmse"], m["mae"], cv_mean)
        except Exception as e:  # noqa: BLE001
            LOG.warning("Model %s failed: %s", name, e)

    metrics = pd.DataFrame(rows).sort_values("r2", ascending=False).reset_index(drop=True)
    metrics_path = config.TABLES_DIR / "strength_model_metrics.csv"
    metrics.to_csv(metrics_path, index=False)
    LOG.info("Saved metrics -> %s", metrics_path)

    # Best model = highest hold-out R2 among non-linear (fallback to any).
    best_name = metrics.iloc[0]["model"]
    best_model = fitted[best_name]

    # Residual std on hold-out (global uncertainty fallback).
    resid = y_te.values - best_model.predict(X_te)
    residual_std = float(np.std(resid))

    # Dedicated uncertainty model: a Random Forest gives a per-sample ensemble
    # spread used as an APPROXIMATE prediction interval, regardless of which model
    # is "best" by accuracy. This is documented as approximate (not calibrated).
    unc_model = fitted.get("RandomForest")
    if unc_model is None:
        unc_model = RandomForestRegressor(n_estimators=200, random_state=config.RANDOM_SEED, n_jobs=-1)
        unc_model.fit(X_tr, y_tr)

    # Persist best model + metadata.
    artefact = {
        "model": best_model,
        "model_name": best_name,
        "uncertainty_model": unc_model,
        "uncertainty_method": "Random Forest ensemble spread (std across trees); approximate, not calibrated",
        "features": feats,
        "residual_std": residual_std,
        "target": config.STRENGTH_TARGET,
        "trained_utc": utils.utc_timestamp(),
        "n_train": int(len(X_tr)),
        "n_test": int(len(X_te)),
    }
    model_path = config.MODELS_DIR / "best_strength_model.pkl"
    joblib.dump(artefact, model_path)
    LOG.info("Saved best model (%s) -> %s", best_name, model_path)

    _plot_comparison(metrics, config.FIGURES_DIR / "strength_model_comparison.png")
    _plot_feature_importance(best_model, feats, best_name,
                             config.FIGURES_DIR / "strength_feature_importance.png")

    return {
        "metrics": metrics, "best_name": best_name, "best_model": best_model,
        "features": feats, "residual_std": residual_std,
        "X_train": X_tr, "X_test": X_te, "y_test": y_te,
    }


def _plot_comparison(metrics: pd.DataFrame, path: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    ax1.barh(metrics["model"], metrics["r2"], color="#2c7fb8")
    ax1.set_xlabel("Hold-out $R^2$"); ax1.set_title("Model comparison — $R^2$ (higher is better)")
    ax1.invert_yaxis(); ax1.set_xlim(0, 1)
    for i, v in enumerate(metrics["r2"]):
        ax1.text(min(v + 0.01, 0.98), i, f"{v:.3f}", va="center", fontsize=8)
    ax2.barh(metrics["model"], metrics["rmse"], color="#de2d26")
    ax2.set_xlabel("Hold-out RMSE (MPa)"); ax2.set_title("Model comparison — RMSE (lower is better)")
    ax2.invert_yaxis()
    for i, v in enumerate(metrics["rmse"]):
        ax2.text(v, i, f" {v:.1f}", va="center", fontsize=8)
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    LOG.info("Saved figure -> %s", path)


def _plot_feature_importance(model, feats: List[str], name: str, path: Path) -> None:
    imp = getattr(model, "feature_importances_", None)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    if imp is not None:
        order = np.argsort(imp)[::-1]
        ax.bar([feats[i] for i in order], imp[order], color="#31a354")
        ax.set_ylabel("Impurity-based importance")
        ax.set_title(f"Feature importance — {name}")
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    else:  # linear model: use absolute standardized coefficients proxy
        coef = getattr(model, "coef_", np.zeros(len(feats)))
        ax.bar(feats, np.abs(coef), color="#31a354")
        ax.set_ylabel("|coefficient|"); ax.set_title(f"Feature weights — {name}")
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
    LOG.info("Saved figure -> %s", path)


if __name__ == "__main__":
    out = train()
    print("Best model:", out["best_name"])
    print(out["metrics"].to_string(index=False))
