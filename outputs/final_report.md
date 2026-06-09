# Final Report

## 1. Project title
AI-Enabled Concrete Performance Passports for OpenBIM: Machine Learning–Based
Quality, Durability, and Sustainability Data Management for Concrete Structures.

## 2. Scientific problem
Concrete performance information is fragmented across labs, mix designs, ML
notebooks, EPD/LCA tools, inspection logs, and BIM models. ML predicts properties
well, but predictions are isolated: not element-bound, not decision-ready
(no explicit uncertainty/evidence), and not interoperable/verifiable.

## 3. Research gap
No standardised, element-level, OpenBIM/IDS-checkable record operationalises ML
predictions (with uncertainty/explanation), optional durability, and EPD-based
carbon benchmarks into an explicit, evidence-ranked QA/QC decision. Adjacent
2025–2026 work advances each piece but none integrates them.

## 4. Contribution statement
A reproducible **data-management methodology** — the Concrete Performance Passport
(CPP) — that integrates concrete ML predictions, uncertainty/risk,
EPD-derived carbon benchmarks, optional durability indicators, data provenance
(evidence levels A–D), and OpenBIM/IDS-ready information requirements into
auditable element-level decision records. **Not a new ML algorithm.**

## 5. Datasets used
- UCI Concrete Compressive Strength (Yeh, 1998); 1030 rows, 8 inputs — cached at
  `data/raw/` and `data/processed/concrete_strength_clean.csv`.
- Compiled U.S. ready-mix concrete EPD dataset (Broyles, Gevaudan & Brown, 2024;
  Mendeley r4jgxk2mhn) — cached at `data/external/concrete_epd_raw.csv` (git-ignored).
- ICE embodied-carbon factors (Hammond & Jones, 2008) — documented in code.

## 6. Methods implemented (code complete)
Data download (offline-capable), cleaning + feature engineering, lightweight ML
(Linear, Random Forest, Extra Trees, Gradient Boosting; XGBoost/LightGBM optional),
approximate uncertainty via RF ensemble spread, evidence ranking + readiness
scoring, rule-based QA/QC decisions, EPD-based carbon benchmarking + ICE estimate,
OpenBIM mapping + proposed Pset + IDS requirement matrix, framework diagram.

## 7. Model performance summary
**PENDING.** Metrics were not regenerated in this emergency pass (no code executed
because pipeline/finalizer repeatedly hung). `model_performance_summary.csv` lists
the candidate models with metrics marked PENDING. No numbers are fabricated.
Reproduce with the offline command in §10.

## 8. Concrete Performance Passport outputs
- Final field schema: `outputs/tables/concrete_performance_passports.csv` (header +
  pending row) and `.json` (field/enum definitions + disclaimer; `passports: []`).
- Authoritative schema in `src/passport_schema.py` (`json_schema()`), schema_version 2.0.
- Demonstration records are **pending** the offline run.

## 9. OpenBIM/IDS outputs
- `outputs/tables/openbim_mapping.csv` — passport field → IFC concept mapping.
- `outputs/tables/ids_requirement_matrix.csv` — 13 IDS-ready requirements.
- Proposed `Pset_ConcretePerformancePassport` (in `src/ifc_mapping.py`; CSV emitted
  by the finalizer). Conceptual IDS XML emitted by `src/ifc_mapping.py`.

## 10. Reproducibility in Google Colab
Open the notebooks in order; each installs dependencies and loads/downloads public
data. Notebook 02 trains the strength model and generates passports; notebook 03
performs carbon benchmarking and OpenBIM/IDS mapping. Notebooks 02/03 are scaffolds
backed by the runnable `src/` modules.

## 11. Local reproduction
```bash
pip install -r requirements.txt
# Offline regeneration of all computed artefacts (uses cached data only):
USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs
```
Do NOT run `python -m src.pipeline` in constrained interactive environments — it
performs cross-validation/SHAP/large reads and hung here. The finalizer is the
supported lightweight path.

## 12. Offline test command
```bash
USE_CACHED_ONLY=1 pytest -q
```
(Tests authored in `tests/test_offline_sanity.py`; not executed in this pass — see
`outputs/test_report.md`.)

## 13. Threats to validity
Dataset bias; UCI dataset age/size; EPD regional bias; illustrative BIM context;
approximate (uncalibrated) uncertainty; durability not modelled; conceptual
OpenBIM/IDS mapping; no real-project validation; no regulatory compliance.

## 14. Limitations
See `outputs/tables/limitations_and_future_work.csv` and chapter §11.

## 15. Exact files generated (this pass; static, no execution)
- Reports: `final_report.md`, `test_report.md`, `final_static_inventory.md`,
  `scientific_novelty_audit.md`, `scientific_evaluation_design.md`,
  `scientific_acceptance_checklist.md`, `pr_description.md`
- Chapter: `chapter/book_chapter_draft.md`
- Tables: `openbim_mapping.csv`, `ids_requirement_matrix.csv`,
  `limitations_and_future_work.csv`, `closest_prior_art_comparison.csv`,
  `model_performance_summary.csv` (pending status),
  `concrete_performance_passports.csv/.json` (schema + pending)
- Pre-existing: literature matrices/summaries, dataset inventory, schema/code,
  notebooks, `dataset_summary.csv`.

## 16. Computed artefacts still PENDING (one offline run)
`outputs/models/best_strength_model.pkl`; `outputs/figures/*.png`
(framework_diagram, strength_model_comparison, strength_feature_importance,
risk_class_distribution, carbon_distribution); real passport records and real
model metrics; `carbon_benchmark_summary.csv`; `durability_data_availability.csv`.

## 17. Remaining recommended work before submission
1. Run the offline finalizer to populate metrics/passports/figures.
2. Run offline tests and record results in `test_report.md`.
3. Fully render notebooks 02/03 with outputs.
4. Optionally export the chapter to DOCX.
5. Supervisor review of scientific framing and references.

## No-overclaim statement
No new ML algorithm, no digital-twin deployment, no official IFC Pset, no
regulatory compliance, no validated durability solution, no real-project
validation, and no "first-ever" claim are made. Computed results are reported only
where regenerated; otherwise marked PENDING.
