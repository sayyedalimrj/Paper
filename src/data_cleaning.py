"""
data_cleaning.py  (Phase 1)
===========================
Normalise the raw concrete strength table to the canonical snake_case schema,
derive engineered features (water/cement, water/binder, total binder, SCM
fraction), validate physical ranges, and write a cleaned CSV to
``data/processed/``.

Implemented in Phase 1. This module is import-safe; running it as a script
performs the cleaning if the raw CSV exists.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

try:
    from src import config, utils
except ImportError:
    import config, utils  # type: ignore

LOG = utils.get_logger("data_cleaning")


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived mix-design features used by the model and passport."""
    df = df.copy()
    binder = (
        df.get("cement", 0)
        + df.get("blast_furnace_slag", 0)
        + df.get("fly_ash", 0)
    )
    df["total_binder"] = binder
    # Guard divide-by-zero.
    safe_cement = df["cement"].replace(0, np.nan)
    safe_binder = binder.replace(0, np.nan)
    df["water_cement_ratio"] = (df["water"] / safe_cement).round(4)
    df["water_binder_ratio"] = (df["water"] / safe_binder).round(4)
    scm = df.get("blast_furnace_slag", 0) + df.get("fly_ash", 0)
    df["scm_fraction"] = (scm / safe_binder).round(4)
    return df


def validate_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """Flag physically implausible rows (kept, not dropped, but logged)."""
    issues = 0
    if "water_cement_ratio" in df:
        bad = df["water_cement_ratio"] > 2.0
        issues += int(bad.sum())
    if "age" in df:
        issues += int((df["age"] <= 0).sum())
    LOG.info("Validation flagged %d potentially anomalous rows.", issues)
    return df


def clean(raw_csv: Optional[Path] = None) -> Optional[Path]:
    config.ensure_dirs()
    raw_csv = Path(raw_csv) if raw_csv else config.RAW_DIR / "concrete_strength_raw.csv"
    if not raw_csv.exists():
        LOG.error("Raw CSV not found: %s (run data_download first)", raw_csv)
        return None
    df = pd.read_csv(raw_csv)
    df = df.dropna(subset=[config.STRENGTH_TARGET]).reset_index(drop=True)
    df = engineer_features(df)
    df = validate_ranges(df)
    out = config.PROCESSED_DIR / "concrete_strength_clean.csv"
    df.to_csv(out, index=False)
    LOG.info("Wrote cleaned CSV -> %s (shape=%s)", out, df.shape)
    return out


if __name__ == "__main__":
    utils.set_seed()
    print("Result:", clean())
