# Scientific Novelty Audit

**Chapter:** AI-Enabled Concrete Performance Passports for OpenBIM — A scientifically
grounded framework for transforming machine-learning predictions, carbon
benchmarks, optional durability indicators, uncertainty/risk, provenance, and
QA/QC decision logic into structured, auditable, OpenBIM/IDS-ready element-level
concrete performance records.

Citation keys refer to `outputs/literature_matrix_updated.csv`.

## 1. What is the exact scientific problem?
Concrete performance information is **fragmented** across silos — laboratory test
sheets, mix designs, machine-learning notebooks, EPD/LCA tools, inspection logs,
and BIM models. Machine learning predicts properties well, but the prediction is
**not bound to a structural element, not risk-typed for a decision, not carrying
its own evidence/provenance, and not expressed in an interoperable, verifiable
form**. There is no standardised, auditable, element-level record that converts
predictions (plus uncertainty, carbon, and optional durability) into a
**decision-ready** artefact for quality, durability, and sustainability
management.

## 2. Why is it important for concrete structures?
Concrete acceptance decisions (accept / review / hold / retest) and sustainability
choices are made per element/pour. Delays and rework arise when the information
needed for those decisions is scattered and arrives late. A structured,
auditable per-element record that fuses predicted performance, confidence,
carbon, and a QA decision — and that can be checked automatically — directly
supports faster, more transparent, and more defensible decisions.

## 3. Why is it not solved by existing concrete ML studies?
They optimise accuracy for a single property and stop at a metric/plot
(`yeh1998`, `springer2026hpcreview`, `fbuil2026hetero`, `screp2026dlllm`).
Outputs are not element-bound, rarely carry decision-ready uncertainty, and are
not interoperable. Even explainable-ML work (`mdpi2025xmlconcrete`) leaves the
explanation in the analysis environment.

## 4. Why is it not solved by existing BIM-QA/QC systems?
They link inspections, checklists, and quality documents to elements
(`mdpi2025qualisite`, `asce2025qms`) but do not embed **predictive** performance,
uncertainty, durability, or carbon, and do not derive a model-informed QA
decision.

## 5. Why is it not solved by Material Passport / Digital Product Passport studies?
MPs/DPPs are **reuse / circularity / end-of-life** centric (`honic2019mp`,
`mdpi2026mppris`, `plos2025concretedpp`, `mdpi2026aipassport`). They inventory
*what material is where for recovery*, not *how an element is predicted to perform
and whether it passes QA now*, with evidence ranking.

## 6. Why is it not solved by existing BIM-LCA/EPD workflows?
They compute embodied carbon and match BIM elements to EPD/LCA data
(`springer2025aibimlca`), but EPD data is weakly represented in IFC
(`mdpi2025epdifc`), integration remains partly manual (`mdpi2026bimlca`), and
carbon is treated **separately** from quality/QA decisions.

## 7. What is the closest prior art?
- `mdpi2026aipassport` — AI applied to material/digital product passports
  (closest *conceptually*, but broad and reuse-oriented).
- `plos2025concretedpp` — a concrete-specific DPP (closest on *concrete
  passports*, but reuse/recycling focus).
- `dt2026qaframework` (preprint) — construction-phase QA digital twin with
  element-level readiness decisions (closest on *QA decisions*, but not
  OpenBIM/IFC/IDS-bound).
- `mdpi2025idscarbon` — applied openBIM IDS for operational carbon (closest on
  *applied IDS for a domain*, but carbon-only).

## 8. Difference between this chapter and the closest prior art
This work sits at the **intersection** none of them occupies: it produces an
**element-level, evidence-ranked, OpenBIM/IDS-checkable** record that fuses
predicted strength + uncertainty/risk + explanation + carbon class + optional
durability + an explicit QA/QC decision, with a proposed
`Pset_ConcretePerformancePassport` and an IDS requirement matrix. It is a
*data-management methodology*, not a single-property predictor, a reuse inventory,
a carbon calculator, or a generic IDS.

## 9. The scientific contribution (not merely software output)
A **reproducible scientific data-management methodology** that:
1. defines a **construct** — the Concrete Performance Passport — with explicit
   dimensions (BIM/element, mix/test, ML outputs, sustainability, decision,
   evidence, OpenBIM refs);
2. introduces an **evidence-ranking scheme (A–D)** and a **readiness/IDS-readiness
   scoring** that make ML-based concrete information *auditable and
   decision-ready*;
3. specifies **information requirements** (IDS-ready) that make the record
   machine-checkable in vendor-neutral OpenBIM workflows;
4. is demonstrated **reproducibly on public data**, with an **ablation-style**
   account of the decision-value added by each layer.

## 10. Claims to avoid
- No new/state-of-the-art ML algorithm or accuracy record.
- No full industrial digital-twin deployment.
- No official IFC property set (the Pset is *proposed*).
- No legal/regulatory (CPR/DPP) compliance.
- No validated durability/service-life solution.
- No real-project validation (public/illustrative data only).
- No "first-ever" primacy.

## Final scientific novelty statement
> This chapter contributes a scientifically structured Concrete Performance
> Passport framework that integrates concrete ML predictions, uncertainty/risk,
> EPD-derived carbon benchmarks, optional durability indicators, data provenance,
> and OpenBIM/IDS-ready information requirements into auditable element-level
> decision records. The novelty is not a new algorithm, but a reproducible
> data-management methodology for transforming fragmented concrete performance
> information into structured quality, durability, and sustainability intelligence
> for concrete structures.
