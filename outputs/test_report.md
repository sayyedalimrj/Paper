# Test Report

## Status: NOT RUN in this emergency finalization pass

**Reason.** The user directed an emergency finalization in which **no project
code is executed** (the full pipeline and the lightweight finalizer repeatedly
hung/timed out in the interactive environment, and code/output files changed
during this pass). Running tests now would either hang or produce a result that is
immediately invalidated by subsequent file changes. Therefore tests were authored
but **not executed**, and no test result is claimed as final.

## What exists
- Offline test suite: `tests/test_offline_sanity.py` (strictly offline; uses tiny
  in-memory fixtures, pure-logic functions, and existing repository files; sets
  `USE_CACHED_ONLY=1`; skips checks for pending computed artefacts).

## Recommended command (to run after the offline finalizer)
```bash
USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs   # regenerate computed artefacts
USE_CACHED_ONLY=1 pytest -q                                    # run offline tests
```

## What the tests verify
- data cleaning works on a tiny fixture (no rows dropped; engineered features);
- risk + QA/QC classification logic (Accept/Review/Hold/Retest/Missing Data);
- passport schema exposes all scientific fields (evidence levels, uncertainty,
  prediction interval, readiness, IDS readiness, decision-support level);
- readiness + IDS-readiness scoring;
- passport JSON is valid and structured; passport CSV has the scientific columns;
- OpenBIM mapping contains IFC concepts (`IfcMaterial`, `Pset_MaterialConcrete`,
  `Pset_ConcretePerformancePassport`);
- IDS matrix contains required information fields and at least one `required` rule;
- model performance summary file exists; chapter draft, final report, README exist;
- a trained-model check that **skips** if the model `.pkl` is pending;
- a guard asserting `USE_CACHED_ONLY=1` so no network is used.

## Superseded prior results
Any earlier pipeline/finalizer partial runs are **superseded** and must not be
treated as final. No previous test result is carried forward.

## Known limitations
- Tests requiring computed artefacts (trained model `.pkl`) are written to **skip**
  until the offline finalizer is run; once run, they validate the saved artefact.
- Tests were validated for structure/imports by static review only in this pass.
