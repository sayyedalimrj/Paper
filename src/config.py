"""
config.py
=========
Central configuration for the AI-Enabled Concrete Performance Passport project.

All paths are resolved relative to the repository root so the code behaves the
same whether it is executed from a local clone, a CI runner, or a Google Colab
session (where the repo is typically cloned into /content/Paper).

Nothing in this module performs I/O at import time except creating output
directories, which is idempotent and safe to call repeatedly.
"""
from __future__ import annotations

import os
from pathlib import Path

# -----------------------------------------------------------------------------
# Repository root resolution
# -----------------------------------------------------------------------------
# This file lives at <repo_root>/src/config.py, so the repo root is two parents
# up. We also allow an override via the CPP_PROJECT_ROOT environment variable,
# which is convenient inside notebooks.
# -----------------------------------------------------------------------------
ENV_ROOT = os.environ.get("CPP_PROJECT_ROOT")
if ENV_ROOT:
    PROJECT_ROOT = Path(ENV_ROOT).resolve()
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]

# -----------------------------------------------------------------------------
# Data directories
# -----------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"

# -----------------------------------------------------------------------------
# Output directories
# -----------------------------------------------------------------------------
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
MODELS_DIR = OUTPUTS_DIR / "models"
CHAPTER_DIR = OUTPUTS_DIR / "chapter"
PASSPORTS_DIR = OUTPUTS_DIR / "passports"

PROGRESS_LOG = OUTPUTS_DIR / "progress_log.md"

# -----------------------------------------------------------------------------
# Reproducibility
# -----------------------------------------------------------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# -----------------------------------------------------------------------------
# Dataset registry
# -----------------------------------------------------------------------------
# Public-only datasets. Each entry documents canonical + mirror URLs so the
# download layer can fall back gracefully if a primary host is unavailable.
# -----------------------------------------------------------------------------
DATASETS = {
    "concrete_strength": {
        "name": "UCI Concrete Compressive Strength (Yeh, 1998)",
        "license": "CC BY 4.0 (UCI Machine Learning Repository)",
        "citation": (
            "Yeh, I-C. (1998). Modeling of strength of high-performance concrete "
            "using artificial neural networks. Cement and Concrete Research, "
            "28(12), 1797-1808."
        ),
        "n_instances": 1030,
        "n_features": 8,
        "urls": [
            # Primary (UCI archive .xls)
            "https://archive.ics.uci.edu/ml/machine-learning-databases/concrete/compressive/Concrete_Data.xls",
            # Mirror (OpenML CSV) handled separately in data_download via sklearn
        ],
        "raw_filename": "Concrete_Data.xls",
    },
}

# -----------------------------------------------------------------------------
# Canonical feature schema for the strength dataset (kg per m^3, except age)
# -----------------------------------------------------------------------------
STRENGTH_FEATURES = [
    "cement",
    "blast_furnace_slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age",
]
STRENGTH_TARGET = "compressive_strength"

# Mapping from raw UCI column names (verbose) to our snake_case schema.
UCI_COLUMN_MAP = {
    "Cement (component 1)(kg in a m^3 mixture)": "cement",
    "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": "blast_furnace_slag",
    "Fly Ash (component 3)(kg in a m^3 mixture)": "fly_ash",
    "Water  (component 4)(kg in a m^3 mixture)": "water",
    "Superplasticizer (component 5)(kg in a m^3 mixture)": "superplasticizer",
    "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": "coarse_aggregate",
    "Fine Aggregate (component 7)(kg in a m^3 mixture)": "fine_aggregate",
    "Age (day)": "age",
    "Concrete compressive strength(MPa, megapascals) ": "compressive_strength",
}

# -----------------------------------------------------------------------------
# Carbon / sustainability benchmark configuration
# -----------------------------------------------------------------------------
# Embodied-carbon (A1-A3 cradle-to-gate, GWP) reference values are documented in
# src/train_carbon_model.py and data/external. These are illustrative, publicly
# sourced industry-average anchors (e.g., NRMCA Industry-Average EPD, ICE
# database). The project NEVER fabricates values: provenance is recorded.
CARBON_CLASS_LABELS = ["Low", "Typical", "High"]

# QA/QC decision categories
QA_DECISIONS = ["Accept", "Review", "Hold", "Retest", "Missing/Insufficient"]


def ensure_dirs() -> None:
    """Create all output/data directories if they do not exist (idempotent)."""
    for d in (
        RAW_DIR,
        PROCESSED_DIR,
        EXTERNAL_DIR,
        FIGURES_DIR,
        TABLES_DIR,
        MODELS_DIR,
        CHAPTER_DIR,
        PASSPORTS_DIR,
    ):
        d.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_dirs()
    print("Project root:", PROJECT_ROOT)
    print("Output dirs ensured.")
