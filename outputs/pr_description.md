# Add AI-enabled Concrete Performance Passport research workflow

## 1. Project title
AI-Enabled Concrete Performance Passports for OpenBIM: Machine Learning–Based
Quality, Durability, and Sustainability Data Management for Concrete Structures.

## 2. Scientific problem
Concrete ML studies often stop at prediction, while BIM/QA/QC systems, Material
Passports/Digital Product Passports, and BIM-LCA workflows do not operationalize
predicted concrete performance as auditable, element-level decision records.
Performance information is fragmented and not interoperable or verifiable.

## 3. Research gap
No standardised, element-level, OpenBIM/IDS-checkable record operationalises ML
predictions (with uncertainty/explanation), optional durability, and EPD-based
carbon benchmarks into an explicit, evidence-ranked QA/QC decision. Adjacent
2025–2026 work advances each piece but none integrates them.

## 4. Contribution statement
A reproducible **data-management methodology** — the Concrete Performance Passport
— integrating ML predictions, uncertainty/risk, EPD-derived carbon benchmarks,
optional durability indicators, provenance (evidence levels A–D), and OpenBIM/IDS
information requirements into auditable element-level decision records. **Not a new
ML algorithm.**

## 5. Datasets used
- UCI Concrete Compressive Strength (Yeh, 1998) — cached.
- Compiled U.S. ready-mix EPD dataset (Broyles, Gevaudan & Brown, 2024) — cached, git-ignored (78 MB).
- ICE embodied-carbon factors (Hammond & Jones, 2008) — documented in code.

## 6. Methods implemented
Offline-capable data loading; cleaning + feature engineering; lightweight ML
(Linear/RF/ExtraTrees/GradientBoosting; XGBoost/LightGBM optional); approximate
uncertainty via RF ensemble spread; evidence ranking + readiness scoring;
rule-based QA/QC decisions; EPD-based carbon benchmarking + ICE estimate; OpenBIM
mapping + proposed `Pset_ConcretePerformancePassport` + IDS requirement matrix.

## 7. Evaluation design
Prediction metrics (R²/RMSE/MAE/MAPE), explainability (feature importance),
decision transformation, readiness/IDS-readiness scoring, carbon benchmarking, and
an ablation-style comparison (prediction → +risk → +evidence → +carbon → full
passport + OpenBIM/IDS). See `outputs/scientific_evaluation_design.md`.

## 8. Key outputs / results
- Final passport **schema** (CSV header + JSON field/enum definitions);
  demonstration records and model metrics are **PENDING one offline run** (no
  numbers fabricated).
- `outputs/tables/openbim_mapping.csv`, `outputs/tables/ids_requirement_matrix.csv`
  (13 requirements), `outputs/closest_prior_art_comparison.csv`,
  `outputs/tables/limitations_and_future_work.csv`.
- Chapter draft `outputs/chapter/book_chapter_draft.md` with all sections.

## 9. Novelty positioning
Sits at the intersection no prior art occupies: element-level, evidence-ranked,
OpenBIM/IDS-checkable fusion of prediction + uncertainty + carbon + optional
durability + QA/QC decision. See `outputs/novelty_positioning.md`,
`outputs/scientific_novelty_audit.md`.

## 10. Threats to validity
Dataset bias; UCI dataset age/size; EPD regional bias; illustrative BIM context;
approximate (uncalibrated) uncertainty; durability not modelled; conceptual
OpenBIM/IDS mapping; no real-project validation; no regulatory compliance.

## 11. Reproducibility instructions
```bash
pip install -r requirements.txt
USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs   # regenerate computed artefacts (offline)
USE_CACHED_ONLY=1 pytest -q                                    # offline tests
```
Do NOT run `python -m src.pipeline` in constrained interactive environments (it
hung here). Use the lightweight finalizer.

## 12. Offline test command and result
Command: `USE_CACHED_ONLY=1 pytest -q`.
Result: **NOT RUN** in this emergency finalization pass (no code executed); tests
authored in `tests/test_offline_sanity.py`. See `outputs/test_report.md`.

## 13. Files generated (this pass)
Reports (`final_report.md`, `test_report.md`, `final_static_inventory.md`,
`scientific_novelty_audit.md`, `scientific_evaluation_design.md`,
`scientific_acceptance_checklist.md`, `pr_description.md`), chapter draft, and
tables (`openbim_mapping.csv`, `ids_requirement_matrix.csv`,
`limitations_and_future_work.csv`, `closest_prior_art_comparison.csv`,
`model_performance_summary.csv` [pending], `concrete_performance_passports.csv/.json`
[schema + pending]). Plus all `src/` modules, notebooks, and literature files.

## 14. Acceptance checklist
See `outputs/scientific_acceptance_checklist.md`. Scientific framing, schema,
mapping, literature, and documentation are complete; computed artefacts (model,
real passport records, figures) are pending one offline finalizer run.

## What is NOT claimed
No new ML algorithm; no full digital twin; no real-project validation; no official
IFC property set; no legal/regulatory compliance; no full durability solution; no
"first-ever" contribution.

## Execution status
The full pipeline and lightweight finalizer were not executed in this pass because
they repeatedly exceeded interactive execution constraints. This PR preserves the
complete scientific and implementation state for review and a single offline
regeneration step.
