"""
data_download.py
================
Download public datasets with graceful fallbacks. Public data only; provenance
is recorded to ``data/raw/provenance.json``.

Primary dataset: UCI Concrete Compressive Strength (Yeh, 1998).
Fallback order:
  1. UCI archive .xls (direct HTTP).
  2. OpenML via scikit-learn (``fetch_openml('Concrete_Data')``).
  3. Local cache if already present.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

try:
    from src import config, utils
except ImportError:  # script execution from within src/
    import config, utils  # type: ignore

LOG = utils.get_logger("data_download")


def _download_http(url: str, dest: Path, timeout: int = 60) -> bool:
    """Try to download a single URL to dest. Returns True on success."""
    import requests

    try:
        LOG.info("Downloading %s", url)
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(resp.content)
        LOG.info("Saved -> %s (%d bytes)", dest, dest.stat().st_size)
        return True
    except Exception as exc:  # noqa: BLE001 - we deliberately catch all
        LOG.warning("HTTP download failed for %s: %s", url, exc)
        return False


def _load_concrete_from_xls(path: Path) -> Optional[pd.DataFrame]:
    try:
        df = pd.read_excel(path)
        df = df.rename(columns={c: config.UCI_COLUMN_MAP.get(c, c) for c in df.columns})
        return df
    except Exception as exc:  # noqa: BLE001
        LOG.warning("Failed to read xls %s: %s", path, exc)
        return None


def _load_concrete_from_openml() -> Optional[pd.DataFrame]:
    """Fallback: fetch from OpenML via scikit-learn."""
    try:
        from sklearn.datasets import fetch_openml

        LOG.info("Falling back to OpenML fetch_openml('Concrete_Data') ...")
        bunch = fetch_openml(name="Concrete_Data", version=1, as_frame=True)
        df = bunch.frame.copy()
        # OpenML column names are typically already terse; map best-effort.
        rename = {}
        lower = {c.lower(): c for c in df.columns}
        wanted = {
            "cement": "cement",
            "blast_furnace_slag": "blast_furnace_slag",
            "fly_ash": "fly_ash",
            "water": "water",
            "superplasticizer": "superplasticizer",
            "coarse_aggregate": "coarse_aggregate",
            "fine_aggregate": "fine_aggregate",
            "age": "age",
            "concrete_compressive_strength": "compressive_strength",
            "strength": "compressive_strength",
        }
        for low, orig in lower.items():
            key = low.replace(" ", "_")
            if key in wanted:
                rename[orig] = wanted[key]
        df = df.rename(columns=rename)
        return df
    except Exception as exc:  # noqa: BLE001
        LOG.warning("OpenML fallback failed: %s", exc)
        return None


def download_concrete_strength() -> Optional[Path]:
    """Ensure the concrete strength dataset is present in data/raw.

    Returns the path to a normalised CSV, or None if all sources fail.
    Honours USE_CACHED_ONLY=1 (offline): only uses cached files, never network.
    """
    import os

    config.ensure_dirs()
    spec = config.DATASETS["concrete_strength"]
    raw_xls = config.RAW_DIR / spec["raw_filename"]
    out_csv = config.RAW_DIR / "concrete_strength_raw.csv"

    if out_csv.exists():
        LOG.info("Cached CSV already present -> %s", out_csv)
        return out_csv

    offline = os.environ.get("USE_CACHED_ONLY", "0") == "1"
    if offline:
        LOG.warning("USE_CACHED_ONLY=1 and no cached CSV at %s — not downloading.", out_csv)
        return None

    df: Optional[pd.DataFrame] = None

    # 1) HTTP .xls
    if not raw_xls.exists():
        for url in spec["urls"]:
            if _download_http(url, raw_xls):
                break
    if raw_xls.exists():
        df = _load_concrete_from_xls(raw_xls)

    # 2) OpenML fallback
    if df is None or df.empty:
        df = _load_concrete_from_openml()

    if df is None or df.empty:
        LOG.error("All download sources failed for concrete strength dataset.")
        return None

    # Keep only known schema columns (in order) where available.
    cols = [c for c in config.STRENGTH_FEATURES + [config.STRENGTH_TARGET] if c in df.columns]
    df = df[cols].apply(pd.to_numeric, errors="coerce")
    df.to_csv(out_csv, index=False)
    LOG.info("Wrote normalised raw CSV -> %s (shape=%s)", out_csv, df.shape)

    # Provenance record
    utils.save_json(
        {
            "dataset": spec["name"],
            "license": spec["license"],
            "citation": spec["citation"],
            "downloaded_utc": utils.utc_timestamp(),
            "rows": int(df.shape[0]),
            "columns": list(df.columns),
            "source_attempts": spec["urls"] + ["OpenML:Concrete_Data"],
        },
        config.RAW_DIR / "provenance.json",
    )
    return out_csv


if __name__ == "__main__":
    utils.set_seed()
    path = download_concrete_strength()
    print("Result:", path)
