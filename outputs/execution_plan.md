# Execution Plan — AI-Enabled Concrete Performance Passports for OpenBIM

This plan breaks the project into small, durable, restartable phases. After each
phase: save outputs to files, update `progress_log.md`, and continue.

## Phase 0 — Setup (DONE)
- Repo structure, `README.md`, `requirements.txt`, `config.py`, `utils.py`,
  `progress_log.md`, this plan.

## Phase 1 — Data layer
- `src/data_download.py`: fetch UCI Concrete Strength (.xls) with OpenML/sklearn
  fallback; record provenance. Stage public carbon benchmarks into
  `data/external/` with documented sources (NRMCA IA-EPD, ICE, GSA/FHWA limits).
- `src/data_cleaning.py`: normalise to snake_case schema, derive `w/c` and
  `w/cm` ratios, total binder, SCM fraction; validate ranges; write
  `data/processed/concrete_strength_clean.csv`.
- **Deliverables:** raw + processed CSVs, data dictionary, provenance JSON.

## Phase 2 — Strength model + explainability
- `src/train_strength_model.py`: train baseline (linear) + gradient boosting
  (XGBoost, fallback to sklearn HistGradientBoosting); 5-fold CV; hold-out
  metrics (R², RMSE, MAE, MAPE); save model + metrics + parity/residual plots.
- `src/explainability.py`: permutation importance + SHAP (fallback to
  impurity/permutation importance if SHAP unavailable); save importance table +
  beeswarm/bar figure.
- Prediction uncertainty: quantile or ensemble-spread → risk category.
- **Deliverables:** `outputs/models/`, metric tables, figures.

## Phase 3 — Passport schema + generation
- `src/passport_schema.py`: dataclasses + JSON Schema for the 6 passport blocks.
- `src/generate_passports.py`: synthesise plausible *element-level* BIM context
  (element IDs/types/quantities) deterministically from seed, attach predictions
  + uncertainty + SHAP top-features + carbon class + QA/QC decision. Clearly
  label which fields are demonstration/illustrative vs. dataset-derived.
- **Deliverables:** `outputs/passports/*.json`, a passport table CSV, sample
  rendered passport (Markdown).

## Phase 4 — Carbon + sustainability
- `src/train_carbon_model.py`: estimate cradle-to-gate GWP per m³ from mix
  composition using published per-constituent embodied-carbon factors (ICE) as a
  transparent linear model — documented, not fabricated. Compare to NRMCA
  strength-class benchmarks → carbon class + percentile.
- **Deliverables:** carbon table, GWP-vs-strength figure, benchmark mapping.

## Phase 5 — OpenBIM / IFC / IDS mapping
- `src/ifc_mapping.py`: map passport fields → IFC concepts; propose
  `Pset_ConcretePerformancePassport`; emit IDS-ready requirement matrix (CSV +
  conceptual IDS XML). `ifcopenshell` optional with conceptual fallback.
- **Deliverables:** mapping table, Pset definition, IDS XML + requirement matrix.

## Phase 6 — Notebooks
- `01_literature_and_dataset_inventory.ipynb` — lit/dataset inventory, download
  checks, tables.
- `02_strength_model_and_passport_generation.ipynb` — runnable end-to-end model
  + passports.
- `03_carbon_and_openbim_mapping.ipynb` — runnable carbon + OpenBIM/IDS.
- Each: markdown, installs, downloads, fallbacks, seeds, outputs to `outputs/`,
  "What this notebook produced" section.

## Phase 7 — Chapter draft
- `outputs/chapter/`: Springer-style chapter (intro, related work, method,
  passport schema, OpenBIM/IDS mapping, case study/results, discussion,
  limitations, conclusion, references). Markdown first; DOCX export attempted
  with fallback to Markdown.

## Phase 8 — Tests + finalisation
- `tests/`: smoke tests for cleaning, schema validation, passport generation,
  mapping. Update README. Push branch / open PR.

### Cross-cutting safe fallbacks
- Dataset unavailable → next-best public dataset, documented.
- Library fails → simpler stable alternative.
- Model fails → simpler baseline.
- DOCX export fails → keep Markdown.
- `ifcopenshell` fails → conceptual mapping + IDS matrices.
