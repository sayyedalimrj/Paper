# AI-Enabled Concrete Performance Passports for OpenBIM: Machine Learning–Based Quality, Durability, and Sustainability Data Management for Concrete Structures

*Final book chapter for the Springer Nature edited volume "Artificial Intelligence in Concrete Structures and Technologies: Concepts, Models, and Applications."*

> **Reproducibility note.** All quantitative results in this chapter were produced by the accompanying open pipeline (`notebooks/concrete_performance_passport_pipeline.ipynb`; `python -m src.pipeline`) on public data, with a fixed random seed (42). The compressive-strength dataset is the UCI dataset (Yeh, 1998; 1,030 mixes). The embodied-carbon benchmarks are derived from the public compiled U.S. ready-mix EPD dataset (Broyles, Gevaudan & Brown, 2024; **43,053 usable records**). Citation keys (e.g., `broyles2024epd`) refer to `outputs/literature_matrix_updated.csv`. No values, citations, or DOIs were fabricated; the conceptual framework is kept distinct from the implemented demonstration throughout.

---

## Abstract

Machine learning (ML) now predicts concrete properties — most maturely compressive strength — with high accuracy. Yet these predictions typically remain isolated numerical outputs: not bound to a structural element, not accompanied by a decision-ready expression of uncertainty or evidence, and not represented in an interoperable, verifiable form for downstream quality, durability, and sustainability decisions. This chapter proposes the **Concrete Performance Passport (CPP)**: a scientifically structured, element-level, auditable record that integrates ML predictions, an approximate uncertainty/risk layer, an evidence/provenance ranking, EPD-derived carbon benchmarks, and an optional durability indicator into an explicit quality-assurance/quality-control (QA/QC) decision, and maps these to OpenBIM concepts (IFC) and a machine-checkable buildingSMART Information Delivery Specification (IDS) requirement set. The contribution is **not a new ML algorithm**; it is a reproducible **data-management methodology** for transforming fragmented concrete performance information into structured decision intelligence.

We demonstrate the workflow end-to-end on public data. A compressive-strength model trained on the UCI dataset attains a held-out coefficient of determination of **R² = 0.924** (RMSE = 4.43 MPa, MAE = 2.91 MPa, MAPE = 9.4%; 5-fold cross-validated R² = 0.931 ± 0.009) using gradient-boosted trees. Permutation importance ranks **age** and **cement** content as the dominant predictors. From 43,053 public EPD records we derive per-strength-class global-warming-potential (GWP) benchmarks (median A1–A3 GWP rising from ≈275 to ≈416 kg CO₂e/m³ across strength classes), which assign each element a Low/Typical/High carbon class. We then generate 30 element-level passports (plus one deliberate missing-data case) that fuse prediction, uncertainty, risk, carbon class, and an explicit QA/QC decision, and we map all passport fields to IFC via a proposed `Pset_ConcretePerformancePassport` (19 properties) and a 13-requirement IDS-ready matrix. We are explicit about limitations: public/illustrative data, an approximate (uncalibrated) uncertainty proxy, an unmodelled durability layer, and a specification-level (not certified) OpenBIM/IDS mapping.

## Keywords

Concrete; machine learning; OpenBIM; IFC; IDS; material passport; digital product passport; embodied carbon; EPD; quality assurance; data management; explainability; uncertainty; sustainability.

---

## 1. Introduction and scientific motivation

Concrete is the most-used construction material, and its quality, durability, and embodied carbon are central to safety and sustainability goals. Over three decades of research have established ML as an effective predictor of concrete properties, beginning with artificial neural networks for high-performance concrete (`yeh1998`) and continuing through ensemble and deep-learning models that routinely report R² > 0.9 for compressive strength (`springer2026hpcreview`, `fbuil2026hetero`, `screp2026dlllm`, `fmats2025hpc`). Durability prediction (carbonation, chloride ingress, shrinkage, creep) is advancing but remains data-limited and heterogeneous (`rilem2025durability`, `springer2025durabilitylca`). Explainability (SHAP/permutation importance) and, increasingly, uncertainty quantification are now common (`mdpi2025xmlconcrete`, `mdpi2026uq`, `uncertaintygwp2025`).

Despite this maturity, a practical gap persists: **the prediction is where the workflow stops.** A predicted strength value is rarely tied to a specific structural element, rarely carries an explicit, decision-ready statement of confidence and evidence, and is almost never expressed in a standardised, machine-checkable form that other project actors and software can consume. The information needed to *accept, review, hold, or retest* a concrete element — and to judge its embodied carbon — is fragmented across laboratory sheets, mix designs, ML notebooks, EPD/LCA tools, inspection logs, and BIM models. **Prediction alone is insufficient for decision-making.**

This chapter addresses that gap by reframing the unit of output from a *number* to an *auditable element-level record*. We define and demonstrate the Concrete Performance Passport (CPP) and show how it can be made OpenBIM/IDS-ready, answering five research questions (Section 3).

## 2. Background

### 2.1 Machine learning for concrete property prediction
The canonical benchmark is the UCI concrete compressive-strength dataset (`yeh1998`; 1,030 mixes, eight inputs). Recent reviews and studies confirm strong accuracy with tree ensembles and deep learning and emphasise interpretability and uncertainty (`springer2026hpcreview`, `mdpi2025xmlconcrete`, `mdpi2026uq`). Durability ML is summarised authoritatively by RILEM TC 315-DCS, which flags data scarcity and weak generalisation (`rilem2025durability`).

### 2.2 BIM/OpenBIM and IFC material data
IFC (ISO 16739) provides open structures for materials (`IfcMaterial`, `IfcMaterialConstituentSet`) and concrete elements (`Pset_ConcreteElementGeneral`, `Pset_MaterialConcrete`) (`bsi_ifcmaterial`, `bsi_psetconcrete`). Recent work argues that IFC/BIM data must be deliberately structured to be usable by AI (`mdpi2024ifcaiready`) and synthesises the open-standard toolset (IFC, COBie, IDS, bSDD, ISO 7817-1 LOIN) (`mdpi2025bimfm`).

### 2.3 Material passports and performance passports
The material passport concept (`honic2019mp`) is dominated by circular-economy, reuse, and end-of-life objectives (`mdpi2026mppris`, `asce2024dimmp`). Digital product passports are reaching concrete (`plos2025concretedpp`) and gaining regulatory momentum (EU CPR DPP; `eu2025cprdpp`). AI applied to passports has been reviewed broadly (`mdpi2026aipassport`) but not as a concrete performance/QA instantiation.

### 2.4 EPD/LCA and concrete sustainability
BIM-LCA integration remains challenged by interoperability and EPD representation in IFC (`mdpi2026bimlca`, `mdpi2025epdifc`); EPD data quality measurably affects ML reliability (`ijlca2026dataquality`). Public EPD data (`broyles2024epd`) and open carbon factors (`hammond2008ice`) enable transparent benchmarking. AI-driven BIM↔LCA matching is emerging but early-stage (`springer2025aibimlca`).

### 2.5 IDS and information requirements
buildingSMART's IDS reached v1.0 (`bsi_ids`); it specifies machine-readable information requirements for automatic IFC checking, complementing the Information Delivery Manual (ISO 29481; `bsi_idm`). Applied IDS for a domain (operational carbon) has been demonstrated (`mdpi2025idscarbon`).

## 3. Research gap and contributions

**Gap.** No standardised, element-level, OpenBIM/IDS-checkable record operationalises concrete ML predictions (with uncertainty and explanation), an optional durability indicator, and EPD-based carbon benchmarking into an explicit, evidence-ranked QA/QC decision. Adjacent 2025–2026 work advances each piece but none integrates them (see `outputs/closest_prior_art_comparison.csv`).

**Research questions.**
- **RQ1.** How can concrete ML predictions be transformed from isolated outputs into structured, auditable performance records for structural elements?
- **RQ2.** What minimum data dimensions are required for an OpenBIM-ready CPP supporting quality, durability, and sustainability decisions?
- **RQ3.** How can uncertainty, provenance, and evidence level improve interpretability and decision-readiness of ML-based concrete predictions?
- **RQ4.** How can EPD-derived carbon benchmarks be integrated with mechanical predictions without overclaiming full mix-design optimisation?
- **RQ5.** What are the practical limitations of implementing such a passport using public datasets and OpenBIM/IDS concepts?

**Contributions.** (C1) the CPP construct and a seven-block data model; (C2) an OpenBIM mapping and a proposed `Pset_ConcretePerformancePassport`; (C3) an IDS-ready requirement matrix and conceptual IDS XML; (C4) a reproducible, public-data demonstration with an evidence-ranking scheme and an ablation-style decision-value analysis.

## 4. Conceptual definition of a Concrete Performance Passport

A **Concrete Performance Passport** is an element-level, auditable data record that binds, for a single concrete element or mix instance:

1. **BIM/element information** — element ID, type, required strength, material class, volume;
2. **mix and test data** — cement, water, SCMs (slag, fly ash, silica fume), aggregates, admixture, age;
3. **ML outputs** — predicted strength, approximate uncertainty/prediction interval, risk class, explanation;
4. **sustainability** — GWP estimate, carbon class, EPD benchmark percentile, durability indicator status;
5. **decision-readiness** — QA/QC decision, readiness score, IDS readiness, decision-support level;
6. **evidence/provenance** — data source type, reference, evidence level A–D, auditability note, DPP/CPR relevance note;
7. **OpenBIM references** — IFC entity, standard Psets, proposed custom Pset, IDS requirement IDs.

It differs from a **material passport** (reuse inventory) and a **digital product passport** (lifecycle/recovery information) by being a **performance and QA** record for the construction/in-service phase, with an explicit evidence ranking (Figure 1).

> **Figure 1.** Scientific workflow: raw concrete data → ML prediction → uncertainty/risk/evidence layer → Concrete Performance Passport → OpenBIM/IDS information requirements → QA/QC and sustainability decision support. (`outputs/figures/framework_diagram.png`)

## 5. Methodology

### 5.1 Datasets
- **Strength:** UCI concrete compressive-strength dataset (`yeh1998`; 1,030 rows, eight mix-design inputs), retrieved and cached locally.
- **Carbon:** compiled U.S. ready-mix EPD dataset (`broyles2024epd`); **43,053 usable records** after filtering to physically plausible ranges, used to derive GWP distributions per strength class. Per-constituent carbon factors from ICE (`hammond2008ice`) support a transparent GWP estimate for mixes without an EPD.

Descriptive statistics of the strength dataset (`outputs/tables/dataset_summary.csv`) confirm a broad design space: cement 102–540 kg/m³ (mean 281), water/binder ratio 0.24–0.90 (mean 0.47), age 1–365 days (median 28), and measured compressive strength 2.3–82.6 MPa (mean 35.8, SD 16.7).

### 5.2 Data cleaning and feature engineering
Columns are normalised to a snake_case schema; engineered features are added (total binder, water/cement and water/binder ratios, SCM fraction); physical ranges are validated. Unit tests run on a tiny in-memory fixture (offline).

### 5.3 ML models and evaluation
A linear baseline is compared against tree ensembles — Random Forest, Extra Trees, Gradient Boosting — plus XGBoost and LightGBM where available. Models are evaluated on a held-out 20% split (R², RMSE, MAE, MAPE) and with 5-fold cross-validation. The best model by held-out R² is persisted together with the feature list, a residual standard deviation, and a dedicated uncertainty model.

### 5.4 Uncertainty and risk
Approximate uncertainty is taken from a Random Forest's **ensemble spread** (standard deviation across trees), yielding an approximate 95% interval (prediction ± 1.96·σ) and a categorical band (Low/Medium/High). This is documented as **approximate, not calibrated**.

### 5.5 Evidence ranking and readiness
Each record carries an **evidence level**: A (measured project/lab data), B (verified public/EPD-derived), C (ML prediction from public data), D (illustrative/missing). A **readiness score** (0–100, required fields weighted double) and an **IDS readiness** status (Pass/Partial/Fail) quantify completeness against required fields.

### 5.6 QA/QC decision logic
Let *r* be the required and *p* the predicted strength, and *u* the relative prediction uncertainty:
`Accept` if *p* ≥ 1.05·*r*; `Review` if *r* ≤ *p* < 1.05·*r*; `Hold` if 0.95·*r* ≤ *p* < *r*; `Retest` if *p* < 0.95·*r* or *u* > 0.20; `Missing Data` if *r* or *p* is unavailable.

### 5.7 Carbon benchmarking
GWP distributions per psi strength class define Low (≤ Q1) / Typical / High (≥ Q3) carbon classes and an EPD benchmark percentile. A transparent ICE-based estimate maps mix composition to cradle-to-gate (A1–A3) GWP for elements without an EPD. No project-level carbon savings are claimed.

### 5.8 OpenBIM mapping and IDS requirements
Passport fields are mapped to IFC concepts (`outputs/tables/openbim_mapping.csv`, 23 mappings), with a proposed `Pset_ConcretePerformancePassport` (19 properties) for fields IFC does not natively cover (prediction, uncertainty, evidence, carbon class, QA decision). A machine-checkable requirement set is expressed as an IDS-ready matrix (13 requirements; `outputs/tables/ids_requirement_matrix.csv`) and a conceptual IDS XML.

## 6. Results

### 6.1 Compressive-strength model performance
Table 1 reports held-out and cross-validated performance. Gradient-boosted trees clearly outperform the linear baseline; **LightGBM is the best model (held-out R² = 0.924)**, marginally ahead of XGBoost, with cross-validated R² of 0.931 ± 0.009 confirming stability. The linear baseline (R² = 0.628) quantifies the value added by non-linear ensembles.

**Table 1.** Compressive-strength model comparison (`outputs/tables/strength_model_metrics.csv`; held-out 20% test split, 5-fold CV). Best model in **bold**.

| Model | R² (hold-out) | RMSE (MPa) | MAE (MPa) | MAPE (%) | CV R² (mean ± SD) |
|---|---|---|---|---|---|
| **LightGBM** | **0.924** | **4.43** | **2.91** | **9.4** | **0.931 ± 0.009** |
| XGBoost | 0.923 | 4.45 | 3.14 | 10.1 | 0.934 ± 0.006 |
| Extra Trees | 0.890 | 5.32 | 3.41 | 10.6 | 0.917 ± 0.015 |
| Gradient Boosting | 0.881 | 5.54 | 4.10 | 13.1 | 0.902 ± 0.014 |
| Random Forest | 0.881 | 5.54 | 3.78 | 12.4 | 0.907 ± 0.016 |
| Linear Regression | 0.628 | 9.80 | 7.75 | 29.3 | 0.601 ± 0.048 |

These values sit squarely in the range reported by the recent literature for this dataset (`springer2026hpcreview`, `fbuil2026hetero`), as expected — the chapter's contribution is the surrounding data structure, not a new accuracy record. (`outputs/figures/strength_model_comparison.png`)

### 6.2 Explainability
Permutation importance on the best model (Table 2) identifies **age** as the dominant predictor by a wide margin, followed by **cement** content, then **water** and **blast-furnace slag** — physically consistent with hydration and water/binder-driven strength development. (`outputs/figures/strength_feature_importance.png`, `outputs/figures/strength_explainability.png`)

**Table 2.** Permutation feature importance (mean decrease in score; `outputs/tables/strength_feature_importance_values.csv`).

| Feature | Importance |
|---|---|
| age | 0.860 |
| cement | 0.488 |
| water | 0.202 |
| blast_furnace_slag | 0.185 |
| superplasticizer | 0.087 |
| fine_aggregate | 0.046 |
| coarse_aggregate | 0.027 |
| fly_ash | 0.003 |

### 6.3 Carbon benchmarking from real EPD data
From 43,053 EPD records we derive per-strength-class A1–A3 GWP benchmarks (Table 3). Median GWP rises monotonically with strength class — from ≈275 kg CO₂e/m³ below 3,000 psi to ≈416 kg CO₂e/m³ at 8,000+ psi — providing a defensible basis for Low/Typical/High classification and percentile placement. An auxiliary model predicting GWP from strength, curing time, and U.S. region attains only R² = 0.289 (RMSE 82.8 kg CO₂e/m³), which we report honestly: the public EPD records lack full mix composition, so strength alone weakly explains embodied carbon — reinforcing that carbon is reported as a benchmarked **class/percentile**, not a precise prediction. (`outputs/figures/carbon_distribution.png`, `outputs/tables/carbon_benchmark_summary.csv`)

**Table 3.** Per-strength-class A1–A3 GWP benchmark (kg CO₂e/m³) from the public EPD dataset (n = 43,053).

| Strength class (psi) | n | Median | Q1 | Q3 |
|---|---|---|---|---|
| <3000 | 2,263 | 275 | 228 | 322 |
| 3000–3999 | 10,564 | 311 | 265 | 364 |
| 4000–4999 | 16,314 | 346 | 296 | 406 |
| 5000–5999 | 8,085 | 377 | 317 | 440 |
| 6000–7999 | 4,168 | 399 | 330 | 470 |
| 8000+ | 1,659 | 416 | 342 | 513 |

### 6.4 Passport demonstration
We generated 30 element-level passports (beams, columns, slabs, walls, footings, piles, bridge decks, piers) plus one deliberate missing-data case (31 records total; `outputs/tables/concrete_performance_passports.csv/.json`, one JSON per element in `outputs/passports/`). Across the demonstration set: predicted strength spans 6.0–76.8 MPa (mean 35.5); mean prediction uncertainty is 5.4 MPa; ICE-estimated GWP spans 146–468 kg CO₂e/m³ (mean 251). The derived decision fields are summarised in Table 4.

**Table 4.** Distribution of decision fields across the 31 demonstration records.

| Field | Distribution |
|---|---|
| Risk class | Low 6, Medium 13, High 11, Unknown 1 |
| QA/QC decision | Accept 19, Retest 11, Missing Data 1 |
| Carbon class | Low 24, Typical 6, High 1 |
| Evidence level | C (ML) 30, D (illustrative/missing) 1 |
| IDS readiness | Pass 30, Partial 1 |
| Decision-support level | prescriptive-lite 30, descriptive 1 |

The single missing-data record (no required strength) correctly degrades to risk class *Unknown*, QA decision *Missing Data*, evidence level *D*, and IDS readiness *Partial* — demonstrating that the schema fails safe rather than fabricating a decision. (`outputs/figures/risk_class_distribution.png`)

### 6.5 OpenBIM/IDS mapping
The mapping table (23 field→IFC mappings) routes standard fields to `IfcMaterial`, `Pset_MaterialConcrete`, `IfcMaterialConstituentSet`, and element subtypes, and routes ML/uncertainty/carbon/QA fields to the proposed `Pset_ConcretePerformancePassport` (19 properties). The IDS-ready matrix specifies 13 requirements (`IDS-CPP-01`…`IDS-CPP-13`), of which 6 are *required* (material/class, specified strength, predicted strength, risk class, QA decision, evidence level) and 7 *optional* (uncertainty, carbon class/value, model reference, prediction interval, readiness score). A conceptual IDS XML (`outputs/chapter/concrete_performance_passport.ids.xml`) illustrates automatic checkability. `ifcopenshell` is an optional dependency; the mapping and IDS artefacts are produced even when it is absent.

## 7. Closest prior art comparison

A structured comparison against ML-only prediction, explainable ML, durability ML, BIM-QA/QC, construction digital twins, BIM-LCA/EPD matching, material/digital product passports, and IFC/IDS frameworks is provided in `outputs/closest_prior_art_comparison.csv`. The CPP is the only configuration that combines ML prediction, uncertainty/risk, carbon, optional durability, QA/QC decision logic, evidence/provenance ranking, element-level decision support, and OpenBIM/IDS mapping. The closest single works — AI-applied-to-passports (`mdpi2026aipassport`), concrete DPP (`plos2025concretedpp`), construction-phase QA digital twins (`dt2026qaframework`, preprint), and applied IDS for operational carbon (`mdpi2025idscarbon`) — each occupy only part of this intersection.

## 8. Evaluation design and ablation

Decision-value is assessed incrementally: prediction only → +risk → +evidence → +carbon → full passport with OpenBIM/IDS. Completeness is quantified via the readiness score and IDS readiness. In the demonstration, complete records reach IDS readiness *Pass* (30/31), while the missing-data record is correctly flagged *Partial* — showing the metric responds to information completeness. Full design in `outputs/scientific_evaluation_design.md`.

## 9. Regulatory-aware and evidence-ranked performance passporting

The CPP is **aligned with** the broader direction of digital product/performance information management in construction (e.g., EU CPR Digital Product Passport; `eu2025cprdpp`) but **claims no legal/regulatory compliance**. The evidence-level scheme (A–D) explicitly separates measured, verified-public/EPD, ML-predicted, and illustrative information, so consumers can calibrate trust and auditability rather than treating all fields as equally reliable. In the demonstration, every ML-derived decision is transparently marked level C, and the illustrative BIM context is marked level D.

## 10. Discussion

The CPP turns ML output into decision intelligence for QA/QC (explicit, explainable, uncertainty-aware decisions), durability management (a provenance-flagged extension point), sustainability management (carbon class on the same record as quality), and BIM/digital-twin integration (vendor-neutral, machine-checkable data). It complements rather than replaces laboratory testing, codes, and engineering judgement. The deliberately modest GWP-from-strength model (R² = 0.289) is itself a finding: it argues against single-variable carbon shortcuts and in favour of benchmarked, percentile-based reporting tied to mix composition.

## 11. Threats to validity and limitations

Dataset scope and age (the UCI dataset uses eight mix-design inputs only — no cement chemistry, aggregate gradation, or curing regime beyond age); EPD regional bias (U.S.-centric); illustrative (level D) BIM context; **approximate, uncalibrated** uncertainty (ensemble spread, not conformal/quantile intervals); durability not modelled (reported as a future extension); conceptual (uncertified) OpenBIM/IFC/IDS mapping; no real-project validation; and no regulatory-compliance claim. See `outputs/tables/limitations_and_future_work.csv`.

## 12. Implications for future research

Validation on real project BIM/QA datasets; integration with laboratory information management systems; certified IFC/IDS validation on real models in tools such as IfcOpenShell/BIMcollab; durability-model expansion with vetted public data; calibrated uncertainty (conformal or quantile regression); and linkage to construction-phase digital twins.

## 13. Conclusion

We presented the Concrete Performance Passport: a reproducible data-management methodology that converts fragmented concrete performance information into structured, auditable, OpenBIM/IDS-ready element-level decision records. On public data, a gradient-boosted strength model (R² = 0.924) and EPD-derived carbon benchmarks (43,053 records) are fused — with uncertainty, an A–D evidence ranking, and an explicit QA/QC decision — into element passports mapped to a proposed `Pset_ConcretePerformancePassport` and a 13-requirement IDS matrix. The novelty lies in integration, evidence ranking, and machine-checkability — not in a new ML algorithm — and is demonstrated transparently on public data with clearly stated limitations.

## Data and code availability

All code, the unified reproducible Colab notebook (`notebooks/concrete_performance_passport_pipeline.ipynb`), and every generated artefact (model metrics, feature importance, carbon benchmarks, passports, OpenBIM/IDS tables, figures) are in the project repository under `outputs/`. The pipeline persists results to Google Drive and is checkpointed for resumable execution. Datasets are public: UCI concrete compressive strength (`yeh1998`) and the compiled U.S. EPD dataset (`broyles2024epd`); carbon factors from ICE (`hammond2008ice`).

## References

Bibliographic details for all citation keys are in `outputs/literature_matrix_updated.csv` (authors, year, title, venue, DOI/URL, source type). Preprints and official documentation are marked as such; no citations or DOIs were fabricated.
