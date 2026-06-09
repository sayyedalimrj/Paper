# AI-Enabled Concrete Performance Passports for OpenBIM: Machine Learning–Based Quality, Durability, and Sustainability Data Management for Concrete Structures

*Draft book chapter for the Springer Nature edited volume "Artificial Intelligence in Concrete Structures and Technologies: Concepts, Models, and Applications."*

> **Status note (transparency).** This is a working academic draft. Quantitative
> results (model metrics, generated passport records, figures) are produced
> reproducibly by the accompanying code (`USE_CACHED_ONLY=1 python -m
> src.finalize_lightweight_outputs`). Where a specific number would appear, the
> draft uses a clearly marked placeholder rather than a fabricated value. The
> chapter consistently distinguishes the **conceptual framework** from the
> **implemented demonstration**. Citation keys (e.g., `mdpi2026aipassport`) refer
> to `outputs/literature_matrix_updated.csv`.

## Abstract
Machine learning (ML) now predicts concrete properties — most maturely
compressive strength — with high accuracy. Yet these predictions typically remain
isolated numerical outputs: not bound to a structural element, not accompanied by
a decision-ready expression of uncertainty or evidence, and not represented in an
interoperable, verifiable form for downstream quality, durability, and
sustainability decisions. This chapter proposes the **Concrete Performance
Passport (CPP)**: a scientifically structured, element-level, auditable record
that integrates ML predictions, an approximate uncertainty/risk layer, an
evidence/provenance ranking, EPD-derived carbon benchmarks, and an optional
durability indicator into an explicit quality-assurance/quality-control (QA/QC)
decision, and maps these to OpenBIM concepts (IFC) and a machine-checkable
buildingSMART Information Delivery Specification (IDS) requirement set. The
contribution is **not a new ML algorithm**; it is a reproducible
**data-management methodology** for transforming fragmented concrete performance
information into structured decision intelligence. We demonstrate the workflow on
public datasets (the UCI concrete compressive-strength dataset and a compiled U.S.
ready-mix EPD dataset) and provide a conceptual OpenBIM/IDS mapping, including a
proposed `Pset_ConcretePerformancePassport`. We are explicit about limitations:
public/illustrative data, an approximate (uncalibrated) uncertainty proxy, an
unmodelled durability layer, and a specification-level (not certified) OpenBIM/IDS
mapping.

## Keywords
Concrete; machine learning; OpenBIM; IFC; IDS; material passport; digital product
passport; embodied carbon; EPD; quality assurance; data management;
explainability; uncertainty; sustainability.

## 1. Introduction and scientific motivation
Concrete is the most-used construction material, and its quality, durability, and
embodied carbon are central to safety and sustainability goals. Over three decades
of research have established ML as an effective predictor of concrete properties,
beginning with artificial neural networks for high-performance concrete
(`yeh1998`) and continuing through ensemble and deep-learning models that routinely
report R² > 0.9 for compressive strength (`springer2026hpcreview`,
`fbuil2026hetero`, `screp2026dlllm`, `fmats2025hpc`). Durability prediction
(carbonation, chloride ingress, shrinkage, creep) is advancing but remains
data-limited and heterogeneous (`rilem2025durability`,
`springer2025durabilitylca`). Explainability (SHAP/permutation importance) and,
increasingly, uncertainty quantification are now common (`mdpi2025xmlconcrete`,
`mdpi2026uq`, `uncertaintygwp2025`).

Despite this maturity, a practical gap persists: **the prediction is where the
workflow stops.** A predicted strength value is rarely tied to a specific
structural element, rarely carries an explicit, decision-ready statement of
confidence and evidence, and is almost never expressed in a standardised,
machine-checkable form that other project actors and software can consume. The
information needed to *accept, review, hold, or retest* a concrete element — and
to judge its embodied carbon — is fragmented across laboratory sheets, mix
designs, ML notebooks, EPD/LCA tools, inspection logs, and BIM models. **Prediction
alone is insufficient for decision-making.**

This chapter addresses that gap by reframing the unit of output from a *number* to
an *auditable element-level record*. We define and demonstrate the Concrete
Performance Passport (CPP) and show how it can be made OpenBIM/IDS-ready.

## 2. Background
### 2.1 Machine learning for concrete property prediction
The canonical benchmark is the UCI concrete compressive-strength dataset
(`yeh1998`; 1030 mixes, eight inputs). Recent reviews and studies confirm strong
accuracy with tree ensembles and deep learning and emphasise interpretability and
uncertainty (`springer2026hpcreview`, `mdpi2025xmlconcrete`, `mdpi2026uq`).
Durability ML is summarised authoritatively by RILEM TC 315-DCS, which flags data
scarcity and weak generalisation (`rilem2025durability`).

### 2.2 BIM/OpenBIM and IFC material data
IFC (ISO 16739) provides open structures for materials (`IfcMaterial`,
`IfcMaterialConstituentSet`) and concrete elements (`Pset_ConcreteElementGeneral`,
`Pset_MaterialConcrete`) (`bsi_ifcmaterial`, `bsi_psetconcrete`). Recent work
argues that IFC/BIM data must be deliberately structured to be usable by AI
(`mdpi2024ifcaiready`) and synthesises the open-standard toolset (IFC, COBie, IDS,
bSDD, ISO 7817-1 LOIN) (`mdpi2025bimfm`).

### 2.3 Material passports and performance passports
The material passport concept (`honic2019mp`) is dominated by circular-economy,
reuse, and end-of-life objectives (`mdpi2026mppris`, `asce2024dimmp`). Digital
product passports are reaching concrete (`plos2025concretedpp`) and gaining
regulatory momentum (EU CPR DPP; `eu2025cprdpp`). AI applied to passports has been
reviewed broadly (`mdpi2026aipassport`) but not as a concrete
performance/QA instantiation.

### 2.4 EPD/LCA and concrete sustainability
BIM-LCA integration remains challenged by interoperability and EPD representation
in IFC (`mdpi2026bimlca`, `mdpi2025epdifc`); EPD data quality measurably affects ML
reliability (`ijlca2026dataquality`). Public EPD data (`broyles2024epd`) and open
carbon factors (`hammond2008ice`) enable transparent benchmarking. AI-driven
BIM↔LCA matching is emerging but early-stage (`springer2025aibimlca`).

### 2.5 IDS and information requirements
buildingSMART's IDS reached v1.0 (`bsi_ids`); it specifies machine-readable
information requirements for automatic IFC checking, complementing the Information
Delivery Manual (ISO 29481; `bsi_idm`). Applied IDS for a domain (operational
carbon) has been demonstrated (`mdpi2025idscarbon`).

## 3. Research gap and contributions
**Gap.** No standardised, element-level, OpenBIM/IDS-checkable record operationalises
concrete ML predictions (with uncertainty and explanation), an optional durability
indicator, and EPD-based carbon benchmarking into an explicit, evidence-ranked QA/QC
decision. Adjacent 2025–2026 work advances each piece but none integrates them
(see `outputs/closest_prior_art_comparison.csv`).

**Research questions.**
- RQ1. How can concrete ML predictions be transformed from isolated outputs into
  structured, auditable performance records for structural elements?
- RQ2. What minimum data dimensions are required for an OpenBIM-ready CPP supporting
  quality, durability, and sustainability decisions?
- RQ3. How can uncertainty, provenance, and evidence level improve interpretability
  and decision-readiness of ML-based concrete predictions?
- RQ4. How can EPD-derived carbon benchmarks be integrated with mechanical
  predictions without overclaiming full mix-design optimisation?
- RQ5. What are the practical limitations of implementing such a passport using
  public datasets and OpenBIM/IDS concepts?

**Contributions.** (C1) the CPP construct and a six/seven-block data model;
(C2) an OpenBIM mapping and a proposed `Pset_ConcretePerformancePassport`;
(C3) an IDS-ready requirement matrix; (C4) a reproducible, public-data
demonstration with an evidence-ranking scheme and ablation-style analysis.

## 4. Conceptual definition of a Concrete Performance Passport
A **Concrete Performance Passport** is an element-level, auditable data record that
binds, for a single concrete element or mix instance:
1. **BIM/element information** (ID, type, required strength, material class, volume);
2. **mix and test data** (cement, water, SCMs, aggregates, admixture, age);
3. **ML outputs** (predicted strength, approximate uncertainty/prediction interval,
   risk class, explanation);
4. **sustainability** (GWP estimate, carbon class, EPD benchmark percentile,
   durability indicator status);
5. **decision-readiness** (QA/QC decision, readiness score, IDS readiness,
   decision-support level);
6. **evidence/provenance** (data source type, reference, evidence level A–D,
   auditability note, DPP/CPR relevance note);
7. **OpenBIM references** (IFC entity, standard Psets, proposed custom Pset, IDS
   requirement IDs).

It differs from a **material passport** (reuse inventory) and a **digital product
passport** (lifecycle/recovery information) by being a **performance and QA** record
for the construction/in-service phase, with an explicit evidence ranking.

## 5. Methodology
### 5.1 Datasets
- **Strength:** UCI concrete compressive-strength dataset (`yeh1998`; 1030 rows,
  eight mix-design inputs), retrieved and cached locally.
- **Carbon:** compiled U.S. ready-mix EPD dataset (`broyles2024epd`); used to derive
  GWP distributions per strength class. Carbon factors from ICE (`hammond2008ice`)
  support a transparent per-constituent GWP estimate.

### 5.2 Data cleaning and feature engineering
Column normalisation to a snake_case schema; engineered features (total binder,
water/cement and water/binder ratios, SCM fraction); range validation. Tests run on
a tiny in-memory fixture (offline).

### 5.3 ML models and evaluation
Baseline (linear) plus tree ensembles (Random Forest, Extra Trees, Gradient
Boosting; XGBoost/LightGBM optional). Held-out evaluation with R², RMSE, MAE, MAPE.
The offline/lightweight configuration uses a single split with reduced model size to
guarantee fast, hang-free reproduction.

### 5.4 Uncertainty and risk
Approximate uncertainty from Random Forest **ensemble spread** (std across trees),
yielding an approximate 95% interval (pred ± 1.96·std) and a categorical band
(Low/Medium/High). This is documented as **approximate, not calibrated**.

### 5.5 Evidence ranking and readiness
Each record carries an **evidence level**: A (measured), B (verified public/EPD),
C (ML prediction from public data), D (illustrative/missing). A **readiness score**
(0–100) and **IDS readiness** (Pass/Partial/Fail) quantify completeness against
required fields.

### 5.6 QA/QC decision logic
`Accept` if predicted ≥ 1.05·required; `Review` if required ≤ predicted < 1.05·required;
`Hold` if 0.95·required ≤ predicted < required; `Retest` if predicted < 0.95·required
or relative uncertainty > 0.20; `Missing Data` if required/predicted unavailable.

### 5.7 Carbon benchmarking
GWP distributions per psi strength class define Low (≤ Q1) / Typical / High (≥ Q3)
carbon classes and an EPD benchmark percentile. A transparent ICE-based estimate maps
mix composition to GWP for elements without an EPD. No project-level carbon savings
are claimed.

### 5.8 OpenBIM mapping and IDS requirements
Passport fields are mapped to IFC concepts (`outputs/tables/openbim_mapping.csv`),
with a proposed `Pset_ConcretePerformancePassport` for fields IFC does not natively
cover (prediction, uncertainty, evidence, carbon class, QA decision). A
machine-checkable requirement set is expressed as an IDS-ready matrix
(`outputs/tables/ids_requirement_matrix.csv`) and a conceptual IDS XML.

## 6. Results (reproducible; values produced by the offline finalizer)
- **Dataset analysis:** descriptive statistics (`outputs/tables/dataset_summary.csv`).
- **Model performance:** R²/RMSE/MAE/MAPE per model and best model
  (`outputs/tables/strength_model_metrics.csv`,
  `outputs/figures/strength_model_comparison.png`). *(Pending one offline run in this
  emergency pass; prior exploratory runs indicated tree ensembles in the typical
  literature range, but no number is asserted here without a regenerated metrics file.)*
- **Explainability:** feature importance (`outputs/figures/strength_feature_importance.png`).
- **Passport demonstration:** records with all scientific fields
  (`outputs/tables/concrete_performance_passports.csv/.json`).
- **OpenBIM/IDS mapping:** mapping table, proposed Pset, IDS requirement matrix.
- **Carbon:** GWP distribution and benchmark summary
  (`outputs/figures/carbon_distribution.png`, `outputs/tables/carbon_benchmark_summary.csv`).

## 7. Closest prior art comparison
A structured comparison against ML-only prediction, explainable ML, durability ML,
BIM-QA/QC, construction digital twins, BIM-LCA/EPD matching, material/digital product
passports, and IFC/IDS frameworks is provided in
`outputs/closest_prior_art_comparison.csv`. The CPP is the only configuration that
combines ML prediction, uncertainty/risk, carbon, optional durability, QA/QC decision
logic, evidence/provenance ranking, element-level decision support, and OpenBIM/IDS
mapping.

## 8. Evaluation design and ablation
Decision-value is assessed incrementally: prediction only → +risk → +evidence →
+carbon → full passport with OpenBIM/IDS. Completeness is quantified via the readiness
score and IDS readiness. Full design in `outputs/scientific_evaluation_design.md`.

## 9. Regulatory-aware and evidence-ranked performance passporting
The CPP is **aligned with** the broader direction of digital product/performance
information management in construction (e.g., EU CPR Digital Product Passport;
`eu2025cprdpp`) but **claims no legal/regulatory compliance**. The evidence-level
scheme (A–D) explicitly separates measured, verified-public/EPD, ML-predicted, and
illustrative information, so consumers can calibrate trust and auditability rather
than treating all fields as equally reliable.

## 10. Discussion
The CPP turns ML output into decision intelligence for QA/QC (explicit, explainable,
uncertainty-aware decisions), durability management (a provenance-flagged extension
point), sustainability management (carbon class on the same record as quality), and
BIM/digital-twin integration (vendor-neutral, machine-checkable data). It complements
rather than replaces laboratory testing, codes, and engineering judgement.

## 11. Threats to validity and limitations
Dataset bias and the age/size of the UCI dataset; EPD regional bias; illustrative
(level D) BIM context; approximate (uncalibrated) uncertainty; durability not modelled;
conceptual (uncertified) OpenBIM/IFC/IDS mapping; no real-project validation; no
regulatory-compliance claim. See `outputs/tables/limitations_and_future_work.csv`.

## 12. Implications for future research
Validation on real project BIM/QA datasets; integration with laboratory information
management systems; certified IFC/IDS validation on real models; durability-model
expansion with vetted public data; calibrated uncertainty (conformal/quantile);
and linkage to construction-phase digital twins.

## 13. Conclusion
We presented the Concrete Performance Passport: a reproducible data-management
methodology that converts fragmented concrete performance information into structured,
auditable, OpenBIM/IDS-ready element-level decision records. The novelty lies in
integration, evidence ranking, and machine-checkability — not in a new ML algorithm —
and is demonstrated transparently on public data with clearly stated limitations.

## References
Bibliographic details for all citation keys are in
`outputs/literature_matrix_updated.csv` (authors, year, title, venue, DOI/URL,
source type). Preprints and official documentation are marked as such; no citations
or DOIs were fabricated.
