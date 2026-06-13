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
# EPD dataset loading  (LOCAL FILE ONLY — online Mendeley download is bypassed)
# -----------------------------------------------------------------------------
# Canonical EPD column headers (present in both the CSV and the XLSX release of
# the public compiled EPD dataset, Broyles et al., 2024).
EPD_COLS = {
    "Concrete Compressive Strength (psi)": "strength_psi",
    "A1-A3 Global Warming Potential (kg CO2-eq)": "gwp_kgco2e_per_m3",
    "Concrete Curation Time": "curation_time",
    "U.S. Region of Plant": "region",
    "Declared Unit": "declared_unit",
}
EPD_FILENAME_HINTS = ("concrete_epd", "compiled_concrete_epd")
EPD_REQUIRED_HEADERS = (
    "Concrete Compressive Strength (psi)",
    "A1-A3 Global Warming Potential (kg CO2-eq)",
)


def _read_tabular(path: Path, **kwargs) -> pd.DataFrame:
    """Read a .csv or .xlsx/.xls file into a DataFrame (XLSX needs openpyxl)."""
    if path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(path, **{k: v for k, v in kwargs.items() if k != "low_memory"})
    return pd.read_csv(path, **kwargs)


def _looks_like_epd(path: Path) -> bool:
    """True if the file is the EPD dataset (by filename hint or header columns)."""
    if path.suffix.lower() not in (".csv", ".xlsx", ".xls"):
        return False
    if any(h in path.name.lower() for h in EPD_FILENAME_HINTS):
        return True
    try:
        head = _read_tabular(path, nrows=0)
        cols = set(map(str, head.columns))
        return all(h in cols for h in EPD_REQUIRED_HEADERS)
    except Exception:  # noqa: BLE001
        return False


def _find_local_epd() -> Optional[Path]:
    """Locate a local EPD data file (CSV or XLSX). NO network access.

    Search order:
      1. ``CPP_EPD_PATH`` environment variable (explicit full path).
      2. The project data directory (``config.DATA_DIR`` — e.g. on Google Drive).
      3. The source repository's own ``data/`` directory (where the file may be
         committed), independent of any ``CPP_PROJECT_ROOT`` override.
    Files whose name matches the known EPD dataset are preferred; otherwise a
    file is accepted only if its header contains the required EPD columns.
    """
    import os

    env = os.environ.get("CPP_EPD_PATH")
    if env and Path(env).exists():
        return Path(env)
    roots = [Path(config.DATA_DIR), Path(__file__).resolve().parents[1] / "data"]
    seen, candidates = set(), []
    for root in roots:
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in (".csv", ".xlsx", ".xls"):
                continue
            rp = p.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            candidates.append(p)
    hinted = [p for p in candidates if any(h in p.name.lower() for h in EPD_FILENAME_HINTS)]
    for p in hinted + [c for c in candidates if c not in hinted]:
        if _looks_like_epd(p):
            return p
    return None


def _finalize_epd(df: pd.DataFrame, note: str) -> Tuple[pd.DataFrame, str]:
    """Normalise columns, coerce numerics, drop implausible rows, bin by class."""
    df = df.rename(columns=EPD_COLS)
    df["strength_psi"] = pd.to_numeric(df.get("strength_psi"), errors="coerce")
    df["gwp_kgco2e_per_m3"] = pd.to_numeric(df.get("gwp_kgco2e_per_m3"), errors="coerce")
    df = df.dropna(subset=["strength_psi", "gwp_kgco2e_per_m3"])
    df = df[(df["strength_psi"].between(500, 20000)) &
            (df["gwp_kgco2e_per_m3"].between(50, 1500))]
    df["strength_class_psi"] = pd.cut(df["strength_psi"], bins=PSI_BINS, labels=PSI_LABELS, right=False)
    LOG.info("EPD usable rows: %d (%s)", len(df), note)
    return df, note


def load_epd() -> Tuple[Optional[pd.DataFrame], str]:
    """Load the REAL EPD dataset from a LOCAL file (CSV or XLSX).

    The online Mendeley API download is intentionally bypassed (it returns HTTP
    403 from some networks). The pipeline reads the dataset the user placed under
    ``data/`` instead, and caches a slim parsed CSV for fast subsequent runs.

    The synthetic stand-in is used ONLY when explicitly permitted
    (``ALLOW_SYNTHETIC_EPD=1`` or ``USE_CACHED_ONLY=1`` for offline tests);
    otherwise a missing dataset raises rather than being silently replaced.
    """
    import os

    cache = config.EXTERNAL_DIR / "concrete_epd_raw.csv"

    # 1) Fast path: a previously-parsed slim CSV cache (real data only).
    if cache.exists():
        try:
            df = pd.read_csv(cache, usecols=lambda c: c in EPD_COLS, low_memory=False)
            if len(df) > 0:
                return _finalize_epd(df, f"cached EPD CSV ({cache})")
        except Exception as e:  # noqa: BLE001
            LOG.warning("Failed reading cached EPD CSV (%s); will re-read the source file.", e)

    # 2) Local source file (CSV or XLSX) — NO network.
    src = _find_local_epd()
    if src is not None:
        LOG.info("Reading local EPD dataset: %s", src)
        raw = _read_tabular(src, low_memory=False)
        keep = [c for c in raw.columns if c in EPD_COLS]
        df = raw[keep].copy()
        # Cache a slim CSV so later runs (and Drive checkpoint reuse) are fast.
        try:
            config.EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
            df.to_csv(cache, index=False)
            LOG.info("Cached slim EPD CSV -> %s", cache)
        except Exception as e:  # noqa: BLE001
            LOG.warning("Could not write EPD CSV cache: %s", e)
        return _finalize_epd(df, f"local EPD file ({src.name})")

    # 3) Synthetic stand-in ONLY when explicitly permitted.
    if os.environ.get("ALLOW_SYNTHETIC_EPD", "0") == "1" or os.environ.get("USE_CACHED_ONLY", "0") == "1":
        LOG.warning("No local EPD file found; using SYNTHETIC stand-in "
                    "(ALLOW_SYNTHETIC_EPD/USE_CACHED_ONLY is set).")
        return _finalize_epd(_synthetic_epd(), "SYNTHETIC fallback (explicitly enabled)")

    raise FileNotFoundError(
        "Real EPD dataset not found and the online download is disabled. Place the "
        "EPD file (CSV or XLSX, e.g. 'Compiled_Concrete_EPD_Data_Version_3_May_1_2024.xlsx') "
        "anywhere under the project 'data/' directory, or set CPP_EPD_PATH to its full "
        "path. To intentionally use a synthetic stand-in, set ALLOW_SYNTHETIC_EPD=1."
    )


# NOTE: The online Mendeley API download helpers were intentionally removed.
# The EPD dataset is now read exclusively from a LOCAL file via load_epd() /
# _find_local_epd() above. This avoids the intermittent HTTP 403 from the
# Mendeley public API and guarantees the real, user-provided dataset is used.


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
