"""
train_carbon_model.py  (Phase 4 — implemented)
==============================================
Two transparent, public-data carbon components (NO fabricated values):

1. EPD benchmark — uses the public compiled U.S. ready-mix concrete EPD dataset
   (Broyles, Gevaudan & Brown 2024; Mendeley r4jgxk2mhn) to derive, per
   compressive-strength class, the GWP distribution (Q1/median/Q3) used to assign
   a carbon class (Low / Typical / High) and an EPD benchmark percentile.

2. ICE estimate — a documented linear estimate of cradle-to-gate (A1-A3) GWP per
   m3 from mix composition using published per-constituent embodied-carbon factors
   (Inventory of Carbon & Energy; Hammond & Jones 2008). This lets us assign a
   carbon class to UCI mixes (which have no EPD) for the passport demonstration.

Outputs:
  * data/external/ice_carbon_factors.csv
  * outputs/tables/carbon_benchmark_summary.csv
  * outputs/figures/carbon_distribution.png
  * outputs/tables/carbon_model_metrics.csv  (optional GWP model)
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from src import config, utils
except ImportError:
    import config, utils  # type: ignore

LOG = utils.get_logger("train_carbon_model")

PSI_PER_MPA = 145.0377

# -----------------------------------------------------------------------------
# ICE embodied-carbon factors (kg CO2e per kg material), cradle-to-gate (A1-A3).
# Representative public values (Hammond & Jones, Inventory of Carbon & Energy).
# These are INDICATIVE generic factors with real uncertainty; documented, not
# fabricated. Superplasticizer/admixture factors are especially uncertain but
# contribute little because admixture masses are small.
# -----------------------------------------------------------------------------
ICE_FACTORS = {
    "cement": 0.83,
    "blast_furnace_slag": 0.083,
    "fly_ash": 0.010,
    "water": 0.001,
    "coarse_aggregate": 0.0048,
    "fine_aggregate": 0.0051,
    "superplasticizer": 1.88,
}
ICE_SOURCE = ("Hammond & Jones (2008), Inventory of Carbon & Energy (ICE); "
              "indicative generic cradle-to-gate (A1-A3) factors.")

# Strength-class bins in psi (US ready-mix convention).
PSI_BINS = [0, 3000, 4000, 5000, 6000, 8000, np.inf]
PSI_LABELS = ["<3000", "3000-3999", "4000-4999", "5000-5999", "6000-7999", "8000+"]


def write_ice_factors() -> Path:
    config.ensure_dirs()
    rows = [{"constituent": k, "kgCO2e_per_kg": v, "source": ICE_SOURCE}
            for k, v in ICE_FACTORS.items()]
    path = config.EXTERNAL_DIR / "ice_carbon_factors.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    LOG.info("Wrote ICE factors -> %s", path)
    return path


def estimate_gwp_from_mix(mix: Dict[str, float]) -> float:
    """Indicative cradle-to-gate GWP (kg CO2e per m3) from mix masses (kg/m3)."""
    return float(sum(ICE_FACTORS.get(k, 0.0) * float(mix.get(k, 0.0) or 0.0)
                     for k in ICE_FACTORS))


# -----------------------------------------------------------------------------
# EPD dataset loading (cached -> download -> synthetic fallback)
# -----------------------------------------------------------------------------
def load_epd() -> Tuple[Optional[pd.DataFrame], str]:
    """Return (clean EPD df with strength_psi + gwp, source_note)."""
    cache = config.EXTERNAL_DIR / "concrete_epd_raw.csv"
    cols = {
        "Concrete Compressive Strength (psi)": "strength_psi",
        "A1-A3 Global Warming Potential (kg CO2-eq)": "gwp_kgco2e_per_m3",
        "Concrete Curation Time": "curation_time",
        "U.S. Region of Plant": "region",
        "Declared Unit": "declared_unit",
    }
    df = None
    if cache.exists():
        try:
            df = pd.read_csv(cache, usecols=lambda c: c in cols, low_memory=False)
            note = "cached EPD CSV (data/external/concrete_epd_raw.csv)"
        except Exception as e:  # noqa: BLE001
            LOG.warning("Failed reading cached EPD: %s", e); df = None
    if df is None:
        import os
        if os.environ.get("USE_CACHED_ONLY", "0") == "1":
            LOG.warning("USE_CACHED_ONLY=1 and no cached EPD CSV — using synthetic fallback (no download).")
            df, note = _synthetic_epd(), "SYNTHETIC fallback (offline; no cached EPD)"
        else:
            df = _download_epd(cache, cols)
            if df is not None:
                note = "downloaded EPD CSV (Mendeley r4jgxk2mhn)"
            else:
                LOG.warning("EPD download failed after retries -> synthetic fallback.")
                df, note = _synthetic_epd(), "SYNTHETIC fallback (download unavailable)"
    df = df.rename(columns=cols)
    df["strength_psi"] = pd.to_numeric(df["strength_psi"], errors="coerce")
    df["gwp_kgco2e_per_m3"] = pd.to_numeric(df["gwp_kgco2e_per_m3"], errors="coerce")
    df = df.dropna(subset=["strength_psi", "gwp_kgco2e_per_m3"])
    # Keep physically plausible rows.
    df = df[(df["strength_psi"].between(500, 20000)) &
            (df["gwp_kgco2e_per_m3"].between(50, 1500))]
    df["strength_class_psi"] = pd.cut(df["strength_psi"], bins=PSI_BINS, labels=PSI_LABELS, right=False)
    LOG.info("EPD usable rows: %d (%s)", len(df), note)
    return df, note


MENDELEY_DATASET = "r4jgxk2mhn"
_HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (concrete-performance-passport research script)",
    "Accept": "application/json, text/csv, */*",
}


def _get_with_retries(url, *, headers=None, timeout=60, retries=4, stream=False):
    """HTTP GET with exponential backoff. Returns a ``requests.Response`` or None."""
    import time as _time

    import requests

    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers or _HTTP_HEADERS,
                                timeout=timeout, stream=stream)
            if resp.status_code == 200:
                return resp
            LOG.warning("GET %s -> HTTP %s (attempt %d/%d)", url, resp.status_code, attempt, retries)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            LOG.warning("GET %s failed (%s) (attempt %d/%d)", url, type(exc).__name__, attempt, retries)
        if attempt < retries:
            _time.sleep(min(2 ** attempt, 20))  # 2,4,8,... capped
    if last_exc is not None:
        LOG.warning("All %d attempts failed for %s: %s", retries, url, last_exc)
    return None


def _mendeley_csv_url() -> Optional[Tuple[str, float]]:
    """Resolve the EPD CSV download URL via the Mendeley public API.

    Tries dataset versions 3 -> 2 -> 1. Validates that responses are JSON before
    parsing (a non-JSON body is what caused the earlier ``Expecting value`` error).
    Returns (download_url, size_bytes) or None.
    """
    for version in (3, 2, 1):
        api = (f"https://data.mendeley.com/public-api/datasets/"
               f"{MENDELEY_DATASET}/files?folder_id=root&version={version}")
        resp = _get_with_retries(api, timeout=60)
        if resp is None:
            continue
        ctype = resp.headers.get("content-type", "")
        if "json" not in ctype.lower():
            LOG.warning("Mendeley API (v%d) returned non-JSON (%s); first 80 chars: %r",
                        version, ctype, resp.text[:80])
            continue
        try:
            files = resp.json()
            csv = next(f for f in files if str(f.get("filename", "")).lower().endswith(".csv"))
            dl = csv["content_details"]["download_url"]
            size = float(csv.get("size", 0) or 0)
            LOG.info("Resolved EPD CSV (v%d): %s (~%.0f MB)", version, csv["filename"], size / 1e6)
            return dl, size
        except Exception as exc:  # noqa: BLE001
            LOG.warning("Could not parse Mendeley file list (v%d): %s", version, exc)
            continue
    return None


def _download_epd(cache: Path, cols: dict) -> Optional[pd.DataFrame]:
    """Download + validate the real EPD CSV. Returns a DataFrame or None.

    The cache file is only written once the bytes are confirmed to parse as a CSV
    containing the expected columns, so a truncated/HTML error response can never
    masquerade as the dataset on a later cached run.
    """
    resolved = _mendeley_csv_url()
    if resolved is None:
        return None
    dl, size = resolved
    LOG.info("Downloading EPD CSV (~%.0f MB) ...", size / 1e6)
    resp = _get_with_retries(dl, timeout=600, retries=3, stream=True)
    if resp is None:
        return None
    try:
        raw = resp.content
    except Exception as exc:  # noqa: BLE001
        LOG.warning("Failed reading EPD response body: %s", exc)
        return None
    # Sanity: a real CSV is multi-MB; an HTML/error page is tiny.
    if len(raw) < 100_000:
        LOG.warning("EPD download too small (%d bytes) — likely an error page, not the CSV.", len(raw))
        return None
    tmp = cache.with_suffix(".tmp")
    tmp.write_bytes(raw)
    try:
        df = pd.read_csv(tmp, usecols=lambda c: c in cols, low_memory=False)
        if "Concrete Compressive Strength (psi)" not in df.columns:
            LOG.warning("Downloaded EPD CSV missing expected columns; discarding.")
            tmp.unlink(missing_ok=True)
            return None
    except Exception as exc:  # noqa: BLE001
        LOG.warning("Downloaded EPD bytes did not parse as CSV (%s); discarding.", exc)
        tmp.unlink(missing_ok=True)
        return None
    tmp.replace(cache)  # atomically promote validated file to the real cache path
    LOG.info("Cached validated EPD CSV -> %s (%d bytes)", cache, cache.stat().st_size)
    return df


def _synthetic_epd(n: int = 2000) -> pd.DataFrame:
    """Tiny clearly-labelled synthetic stand-in (only used if download fails)."""
    rng = np.random.default_rng(config.RANDOM_SEED)
    psi = rng.normal(4200, 1400, n).clip(2000, 9000)
    gwp = 120 + 0.045 * psi + rng.normal(0, 45, n)
    return pd.DataFrame({
        "Concrete Compressive Strength (psi)": psi,
        "A1-A3 Global Warming Potential (kg CO2-eq)": gwp.clip(120, 800),
        "Concrete Curation Time": rng.choice([28, 56], n),
        "U.S. Region of Plant": "synthetic",
        "Declared Unit": "1 m3 of concrete",
    })


def build_benchmarks(df: pd.DataFrame) -> pd.DataFrame:
    """Per strength-class GWP quartiles -> carbon-class thresholds."""
    g = df.groupby("strength_class_psi", observed=True)["gwp_kgco2e_per_m3"]
    summary = g.agg(n="count", mean="mean", median="median",
                    q1=lambda s: s.quantile(0.25),
                    q3=lambda s: s.quantile(0.75),
                    min="min", max="max").reset_index()
    summary = summary.round(1)
    path = config.TABLES_DIR / "carbon_benchmark_summary.csv"
    summary.to_csv(path, index=False)
    LOG.info("Saved carbon benchmark summary -> %s", path)
    return summary


def classify_carbon(gwp: Optional[float], strength_psi: Optional[float],
                    df: pd.DataFrame, summary: pd.DataFrame) -> Tuple[str, Optional[float], str]:
    """Return (carbon_class, percentile_within_group, group_label)."""
    if gwp is None or strength_psi is None:
        return "Not assessed", None, "n/a"
    label = pd.cut([strength_psi], bins=PSI_BINS, labels=PSI_LABELS, right=False)[0]
    if label is None or pd.isna(label):
        return "Not assessed", None, "n/a"
    grp = df[df["strength_class_psi"] == label]["gwp_kgco2e_per_m3"]
    if len(grp) < 20:  # too few to benchmark -> use whole dataset
        grp = df["gwp_kgco2e_per_m3"]; group_label = "all (sparse class)"
    else:
        group_label = str(label)
    q1, q3 = grp.quantile(0.25), grp.quantile(0.75)
    pct = float((grp < gwp).mean() * 100.0)
    if gwp <= q1:
        cls = "Low"
    elif gwp >= q3:
        cls = "High"
    else:
        cls = "Typical"
    return cls, round(pct, 1), group_label


def plot_distribution(df: pd.DataFrame) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    ax1.hist(df["gwp_kgco2e_per_m3"], bins=50, color="#41ab5d", edgecolor="white")
    ax1.set_xlabel("A1-A3 GWP (kg CO$_2$e / m$^3$)"); ax1.set_ylabel("count")
    ax1.set_title(f"Concrete EPD GWP distribution (n={len(df):,})")
    order = [l for l in PSI_LABELS if l in set(df["strength_class_psi"].astype(str))]
    data = [df[df["strength_class_psi"].astype(str) == l]["gwp_kgco2e_per_m3"] for l in order]
    # matplotlib renamed boxplot's ``labels`` kwarg to ``tick_labels`` in 3.9;
    # set tick labels manually so the figure renders on any version.
    ax2.boxplot(data, showfliers=False)
    ax2.set_xticks(range(1, len(order) + 1))
    ax2.set_xticklabels(order)
    ax2.set_xlabel("Strength class (psi)"); ax2.set_ylabel("GWP (kg CO$_2$e / m$^3$)")
    ax2.set_title("GWP by strength class"); plt.setp(ax2.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout(); fig.savefig(config.FIGURES_DIR / "carbon_distribution.png",
                                    dpi=150, bbox_inches="tight"); plt.close(fig)
    LOG.info("Saved figure -> outputs/figures/carbon_distribution.png")


def train_gwp_model(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Optional: predict GWP from strength(psi)+curation+region (EPD-available features)."""
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split

        d = df.copy()
        d["curation_time"] = pd.to_numeric(d.get("curation_time"), errors="coerce").fillna(28)
        d["region"] = d.get("region", "unknown").astype(str)
        X = pd.get_dummies(d[["strength_psi", "curation_time", "region"]],
                           columns=["region"], drop_first=True)
        y = d["gwp_kgco2e_per_m3"]
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=config.RANDOM_SEED)
        model = RandomForestRegressor(n_estimators=300, random_state=config.RANDOM_SEED, n_jobs=-1)
        model.fit(Xtr, ytr)
        m = utils.regression_metrics(yte, model.predict(Xte))
        out = pd.DataFrame([{"model": "RandomForest (GWP ~ strength+curation+region)",
                             "r2": round(m["r2"], 3), "rmse": round(m["rmse"], 1),
                             "mae": round(m["mae"], 1), "mape": round(m["mape"], 1),
                             "n_features": X.shape[1], "note":
                             "EPD lacks full mix composition; modest R2 expected"}])
        out.to_csv(config.TABLES_DIR / "carbon_model_metrics.csv", index=False)
        LOG.info("Saved GWP model metrics (R2=%.3f) -> outputs/tables/carbon_model_metrics.csv", m["r2"])
        return out
    except Exception as e:  # noqa: BLE001
        LOG.warning("GWP model training skipped (%s).", e)
        return None


def run() -> Dict:
    config.ensure_dirs(); utils.set_seed()
    write_ice_factors()
    df, note = load_epd()
    summary = build_benchmarks(df)
    plot_distribution(df)
    model_metrics = train_gwp_model(df)
    is_synthetic = "SYNTHETIC" in note.upper()
    # Persist a provenance marker so downstream steps (e.g. the notebook) can tell
    # whether the carbon benchmark used the real EPD dataset or a synthetic stand-in.
    utils.save_json(
        {
            "source_note": note,
            "is_synthetic": is_synthetic,
            "n_rows": int(len(df)),
            "generated_utc": utils.utc_timestamp(),
        },
        config.TABLES_DIR / "carbon_source.json",
    )
    if is_synthetic:
        LOG.warning("Carbon benchmark built from SYNTHETIC data — real EPD download "
                    "was unavailable. Re-run when online to use the real dataset.")
    return {"epd": df, "summary": summary, "source_note": note,
            "gwp_model": model_metrics, "is_synthetic": is_synthetic}


if __name__ == "__main__":
    r = run()
    print("EPD source:", r["source_note"])
    print(r["summary"].to_string(index=False))
