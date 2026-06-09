# Scientific Evaluation Design

**Chapter:** AI-Enabled Concrete Performance Passports for OpenBIM

This document defines how the framework is evaluated. It is the evaluation
*design*; the quantitative results are produced reproducibly by the offline
finalizer (`USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs`). In
the emergency finalization pass no code was executed, so numeric results are
reported as **pending**; no values are fabricated.

## 1. Prediction performance
- **Metrics:** R², RMSE, MAE, MAPE on a held-out test split (20%).
- **Cross-validation:** optional; in the lightweight/offline configuration a
  single train/test split is used (CV omitted to avoid the interactive hang).
- **Models compared:** Linear Regression (baseline), Random Forest, Extra Trees,
  Gradient Boosting (XGBoost/LightGBM optional if installed). Lightweight settings
  (<=50 trees) for fast offline reproduction.
- **Artefacts:** `outputs/tables/strength_model_metrics.csv`,
  `outputs/tables/model_performance_summary.csv`,
  `outputs/figures/strength_model_comparison.png`.

## 2. Explainability
- **Method:** impurity-based feature importance (lightweight; SHAP intentionally
  skipped to avoid runtime hangs). Permutation importance is available as an
  alternative.
- **Engineering plausibility check:** confirm dominant features align with
  domain knowledge (e.g., cement content, age, water/binder ratio).
- **Artefacts:** `outputs/figures/strength_feature_importance.png`,
  `outputs/figures/strength_explainability.png`,
  `outputs/tables/strength_feature_importance_values.csv`.

## 3. Decision transformation
- Show how a raw predicted strength becomes a QA/QC decision via explicit rules
  (Accept / Review / Hold / Retest / Missing Data) using required vs predicted
  strength and relative uncertainty.
- Compare "prediction only" vs "passport record" in information content and
  decision-readiness.

## 4. Passport completeness
- **Readiness score (0–100):** weighted completeness of required + recommended
  fields.
- **IDS readiness:** Pass / Partial / Fail against required IDS fields.
- **Missing-field analysis:** which required fields are absent and the effect on
  the decision (e.g., missing required strength -> Missing Data).

## 5. Carbon benchmark
- **GWP distribution by strength class** from the public EPD dataset (Broyles et
  al. 2024): quartiles per psi class define Low/Typical/High carbon classes and
  an EPD benchmark percentile.
- **No project-level carbon savings are claimed** (no real project volumes/mixes).
- **Artefacts:** `outputs/tables/carbon_benchmark_summary.csv`,
  `outputs/figures/carbon_distribution.png`.

## 6. Uncertainty / risk
- **Proxy:** Random Forest ensemble spread (std across trees) -> approximate 95%
  interval (pred ± 1.96·std); residual std fallback. Documented as **approximate,
  not calibrated**. Categorical band (Low/Medium/High) also reported.
- **Limitation:** not a calibrated predictive interval; conformal/quantile
  methods are future work.

## 7. Ablation-style comparison (decision-value of each layer)
| Configuration | Content | Decision value |
|---|---|---|
| Baseline A | strength prediction only | a number; no decision |
| Baseline B | A + risk class | prioritisation possible |
| Baseline C | B + evidence/provenance (A–D) | auditable; trust calibrated |
| Baseline D | C + carbon class | joint quality+sustainability view |
| Proposed | full passport + OpenBIM/IDS mapping | element-level, vendor-neutral, machine-checkable decision record |

## 8. Threats to validity
- **Dataset bias / construct validity:** UCI dataset age (1998) and size (1030),
  limited inputs; benchmark may not reflect modern SCM-rich mixes.
- **External validity:** EPD dataset is U.S.-centric (regional bias); BIM element
  context is illustrative (evidence level D), not a real project.
- **Internal validity:** uncertainty is an approximate ensemble-spread proxy.
- **Implementation validity:** OpenBIM/IFC/IDS mapping is conceptual unless
  validated on real IFC files with certified IDS tooling.
- **Durability:** not fully modelled (no clean public dataset cached); reported as
  future extension.
- **Regulatory interpretation:** DPP/CPR alignment is conceptual; no compliance
  claimed.
