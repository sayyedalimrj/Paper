# Scientific Acceptance Checklist

Honest status as of the emergency finalization pass (no code executed this pass).
Legend: ✅ done · 🟡 partial/pending one offline run · ❌ not done.

| # | Criterion | Status | Evidence / note |
|---|---|---|---|
| 1 | Clear research gap exists | ✅ | `research_gap_and_contributions.md`, `scientific_novelty_audit.md` |
| 2 | Closest prior art compared | ✅ | `closest_prior_art_comparison.csv` |
| 3 | Scientific novelty stated without overclaim | ✅ | `novelty_positioning.md`, `scientific_novelty_audit.md` |
| 4 | Research questions defined (RQ1–RQ5) | ✅ | chapter §3; `research_gap_and_contributions.md` |
| 5 | Datasets documented | ✅ | `dataset_inventory.md/.csv`, `data/raw/provenance.json` |
| 6 | ML model trained and evaluated | 🟡 | code complete; metrics PENDING one offline run (`model_performance_summary.csv` marked pending) |
| 7 | Baselines compared (ablation) | ✅ (design) / 🟡 (numbers) | `scientific_evaluation_design.md` §7 |
| 8 | Explainability included | 🟡 | impurity importance in code; figure pending offline run |
| 9 | Uncertainty/risk included or limitation documented | ✅ | ensemble-spread proxy in schema/code; documented as approximate |
| 10 | Evidence/provenance layer included | ✅ | evidence levels A–D in `passport_schema.py`, mapping, IDS matrix |
| 11 | Carbon benchmark included or limitation documented | 🟡 | EPD cached + code complete; summary/figure pending offline run |
| 12 | Durability layer included or limitation documented | ✅ | documented as future extension (`durability_data_availability` design; limitations table) |
| 13 | OpenBIM/IDS mapping included | ✅ | `openbim_mapping.csv`, `ids_requirement_matrix.csv`, proposed Pset |
| 14 | Threats to validity included | ✅ | chapter §11; `scientific_evaluation_design.md` §8 |
| 15 | Limitations included | ✅ | `limitations_and_future_work.csv` |
| 16 | Chapter distinguishes conceptual vs implemented | ✅ | chapter status note + §6 placeholders |
| 17 | No fake citations | ✅ | literature matrices; preprints/official docs flagged |
| 18 | No fake results | ✅ | metrics/passport records marked PENDING; no numbers fabricated |
| 19 | Colab notebooks runnable or documented | 🟡 | notebooks present; 02/03 are scaffolds backed by runnable `src/` modules |
| 20 | Final report complete | ✅ | `final_report.md` |
| 21 | Offline tests run | 🟡 | tests authored; NOT run in emergency pass (see `test_report.md`); command provided |
| 22 | PR-ready status | ✅ | branch + `pr_description.md` prepared |

## Summary
The **scientific framing, schema, mapping, literature, and documentation are
complete**. The **computed artefacts** (trained model, real passport records,
figures) are **pending a single offline run** of
`USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs`, which was not
executed in this pass because pipeline/finalizer execution repeatedly hung in the
interactive environment. No results are fabricated.
