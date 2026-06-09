# Final Static Inventory

**Date:** 2026-06-09 · **Mode:** emergency finalization (static only — no code executed).

> Why: the full pipeline (`python -m src.pipeline`) and the lightweight finalizer
> (`src/finalize_lightweight_outputs.py`) repeatedly exceeded the interactive
> execution constraints (hung/timed out). To deliver a clean, reviewable state,
> this pass performs **no code execution**: it inventories existing work, authors
> honest documentation, writes the deterministic (non-computed) tables, and marks
> computed artefacts (trained model, passport records, figures) as **pending
> reproduction** via the documented offline commands. No results are fabricated.

## Source files (present)
- `src/`: `config.py`, `utils.py`, `data_download.py`, `data_cleaning.py`,
  `train_strength_model.py`, `train_durability_model.py`, `train_carbon_model.py`,
  `explainability.py`, `passport_schema.py`, `generate_passports.py`,
  `ifc_mapping.py`, `pipeline.py`, `finalize_lightweight_outputs.py`, `__init__.py`
- All modules updated with the scientific schema (evidence levels, uncertainty,
  readiness scoring, IDS readiness, decision-support level, carbon class,
  durability status, DPP/CPR note) and an offline `USE_CACHED_ONLY` mode.

## Notebooks (present)
- `notebooks/01_literature_and_dataset_inventory.ipynb` (populated, runnable checks)
- `notebooks/02_strength_model_and_passport_generation.ipynb` (scaffold + "what it produces")
- `notebooks/03_carbon_and_openbim_mapping.ipynb` (scaffold + "what it produces")

## Literature / scientific framing (present)
- `outputs/literature_matrix.csv` (35 sources) and `outputs/literature_matrix_updated.csv` (41 sources, richer columns)
- `outputs/literature_summary.md`, `outputs/recent_literature_update_2025_2026.md`
- `outputs/source_quality_audit.md`, `outputs/novelty_positioning.md`
- `outputs/research_gap_and_contributions.md`, `outputs/chapter_evidence_map.md`
- `outputs/dataset_inventory.md` / `.csv`, `outputs/execution_plan.md`, `outputs/progress_log.md`

## Output tables
- **Present:** `outputs/tables/dataset_summary.csv`
- **Authored this pass (deterministic, not computed):**
  `openbim_mapping.csv`, `ids_requirement_matrix.csv`,
  `limitations_and_future_work.csv`, `closest_prior_art_comparison.csv`,
  `model_performance_summary.csv` (status row; **no fabricated metrics**)
- **Authored this pass (schema + disclaimer, demonstration records pending):**
  `concrete_performance_passports.csv`, `concrete_performance_passports.json`

## Cached data (present; large files git-ignored)
- `data/raw/Concrete_Data.xls` (124K), `data/raw/concrete_strength_raw.csv` (60K),
  `data/raw/provenance.json`
- `data/processed/concrete_strength_clean.csv` (84K)
- `data/external/concrete_epd_raw.csv` (78M, **git-ignored**; reproducible)

## Computed artefacts — PENDING (require one offline run)
- `outputs/models/best_strength_model.pkl` — **pending** (run finalizer)
- `outputs/figures/*.png` (framework_diagram, strength_model_comparison,
  strength_feature_importance, risk_class_distribution, carbon_distribution) — **pending**
- Real passport demonstration records + real model metrics — **pending**

## How to reproduce the pending artefacts (offline, one command)
```bash
USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs
```
(Uses cached data only; no downloads, no SHAP, no cross-validation; lightweight
models. Designed to complete in well under two minutes outside the interactive
execution constraints that caused the hangs here.)
