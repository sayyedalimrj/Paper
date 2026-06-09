# Literature Summary

**Chapter:** AI-Enabled Concrete Performance Passports for OpenBIM — Machine Learning–Based Quality, Durability, and Sustainability Data Management for Concrete Structures

This summary synthesises the 35 sources catalogued in `literature_matrix.csv`
(areas A–F). All sources were located through web search of reliable venues
(Springer, Nature, Elsevier/ScienceDirect, MDPI, Frontiers, buildingSMART, UCI,
Mendeley Data, ASCE, ASTM, RILEM). No references or dataset properties were
fabricated; where author lists could not be reliably confirmed from the source,
the entry is marked `(see DOI/URL)` rather than inventing names.

> Compliance note: source content below is paraphrased and summarised for
> licensing compliance; see the matrix for citations and links.

---

## A. What has already been done?

### Machine learning for concrete properties
Concrete property prediction is one of the most mature applications of ML in
civil engineering. Since Yeh's foundational ANN model and the canonical
1030-mix benchmark dataset (`yeh1998`), hundreds of studies have predicted
**compressive strength** with neural networks, tree ensembles (random forest,
XGBoost, gradient boosting), and hybrid/metaheuristic-optimised models, often
reporting R² > 0.9 on the same UCI data (`fmats2025hpc`, `springer2024compare`,
`screp2024gui`). The field has extended to **durability** — chloride
migration/diffusion, carbonation, sulfate attack, frost damage, shrinkage, and
corrosion — consolidated in the RILEM TC 315-DCS review (`rilem2025durability`)
and individual studies (`fmats2024chloride`, `hosseinzadeh2023chloride`,
`rilem2024carbonation`). **Multi-property / multi-output** frameworks now predict
several mechanical and durability targets jointly (`prayogo2025scmrac`,
`screp2025multitask`). **Explainable ML** (SHAP, LIME, PDP) is increasingly
standard for exposing feature importance (`mdpi2025xmlconcrete`,
`screp2025multitask`). On sustainability, ML predicts **GWP/embodied carbon**
alongside strength, sometimes with **calibrated uncertainty** (`uncertaintygwp2025`
— strength + GWP with jackknife intervals on 3114 mixes; `springer2025lowcarbonreview`).

### BIM / OpenBIM / IFC for concrete data management
IFC (ISO 16739) provides open, standardised structures for materials
(`IfcMaterial`) and concrete elements (`Pset_ConcreteElementGeneral`,
`Pset_PrecastConcreteElementFabrication`) (`bsi_ifcmaterial`, `bsi_psetconcrete`).
BIM-based **QA/QC** systems link field inspections and quality documents to model
elements (`mdpi2025qualisite` QualiSite/ISO 9001; `asce2025qms`;
`springer2022bimreview`).

### Material passports
The **material passport (MP)** concept — buildings as material banks — is well
established (`honic2019mp`) and dominated by **circular-economy, reuse, and
end-of-life (EOL)** objectives (`asce2024dimmp`, `mdpi2026mp`,
`mdpi2026builtasset`, `emerald2024turkmp`).

### BIM + LCA / EPD / sustainability
A large literature integrates **BIM with LCA** for embodied-carbon assessment,
but reviews repeatedly find workflows manual, spreadsheet-based, and hampered by
interoperability gaps (`obrecht2020bimlca`, `mdpi2026bimlca`). Recent work shows
**EPD data is hard to represent inside IFC** (`mdpi2025epdifc`) and that **EPD
data quality materially affects ML reliability** (`ijlca2026dataquality`). Public
**EPD datasets** now exist at scale (`broyles2024epd`) and open carbon-factor
inventories such as ICE are available (`hammond2008ice`).

### Construction-phase digital twins & QA/QC decision support
Early-age strength prediction (maturity method ASTM C1074 `astm_c1074`; IoT+ANN
`screp2025earlyage`) supports **release/hold/retest** decisions such as formwork
removal. A recent **construction-phase digital twin** framework links inspection,
production, early-age sensing, and predictive strength to individual elements for
readiness-based QA decisions (`dt2026qaframework`), and BIM has been shown to
carry construction-phase sensor data (`mdpi2020formwork`).

### IDS and information requirements
buildingSMART's **Information Delivery Specification (IDS)** became a final
standard (v1.0, 2024) for defining machine-readable information requirements and
**automatically checking IFC models** (`bsi_ids`), complementing the Information
Delivery Manual / ISO 29481 (`bsi_idm`).

---

## Where does each stream usually stop?

- **ML concrete studies usually stop at a number.** They report accuracy metrics
  (and sometimes a SHAP plot or a standalone GUI) for a single property. The
  prediction is rarely attached to a *structural element*, rarely carries
  *uncertainty/risk* into a decision, and is almost never expressed in an
  *interoperable, standardised data structure*. The output dies in a notebook.

- **BIM/QC systems usually stop at inspection and document management.** They
  link checklists, photos, and quality documents to elements, but do not embed
  *predictive* material performance, durability risk, or carbon class.

- **Material passports usually stop at reuse / end-of-life.** They inventory
  *what material is where* for future recovery, not *how the material is
  expected to perform* (strength, durability, with what confidence) nor its QA
  acceptance status during construction.

- **BIM-LCA/EPD work usually stops at carbon accounting.** It computes embodied
  carbon, but EPD/GWP data remains weakly represented in IFC and disconnected
  from quality and durability decisions for the same element.

- **Digital-twin QA frameworks** are emerging and element-aware, but are not yet
  expressed through **OpenBIM IFC/IDS** standards, limiting vendor-neutral
  exchange and automated requirement checking.

---

## What are the remaining gaps?

1. **No standardised, element-level carrier** unifies ML predictions, prediction
   uncertainty/risk, durability indicators, carbon class, and a QA/QC decision.
2. **ML outputs are not OpenBIM-ready**: predictions, uncertainty, SHAP
   explanations, and carbon class have no agreed IFC property representation;
   EPD data itself is hard to embed in IFC (`mdpi2025epdifc`).
3. **Material passports are reuse-centric**, not performance/quality/durability/
   sustainability-centric for the *in-service and construction* phases.
4. **Information requirements are not formalised**: there is no IDS-ready
   requirement set describing *what a concrete element must declare* about its
   predicted performance, carbon, and QA status.

---

## Why is a Concrete Performance Passport useful?

It packages, **per element/mix**, the things that today live in separate silos
(lab sheet, mix design, ML notebook, EPD/LCA tool, inspection log, BIM model)
into one structured, validated record that:

- carries the **ML prediction + uncertainty + explanation** next to the
  **required strength**, enabling an explicit **Accept / Review / Hold / Retest /
  Missing-data** decision;
- attaches a **carbon class and EPD-based benchmark percentile**, connecting
  quality and sustainability for the same element;
- is **mapped to IFC concepts** (`IfcMaterial`, `Pset_MaterialConcrete`) plus a
  proposed `Pset_ConcretePerformancePassport`, and is **checkable via IDS**.

This turns one-off predictions into reusable, auditable, vendor-neutral data
management — addressing the interoperability and "output dies in a notebook"
gaps above.

---

## Why is this suitable for a book chapter?

- It is **integrative and practical** rather than a single novel algorithm: it
  connects four mature literatures (ML for concrete, BIM/IFC, material passports,
  BIM-LCA/EPD) and one emerging one (construction-phase digital twins) into a
  reproducible workflow.
- It can be **fully demonstrated on public data** (UCI strength dataset; public
  EPD dataset; ICE factors) and standard, open tools — ideal for a didactic,
  reproducible chapter aimed at researchers and practitioners.
- It is **standards-anchored** (IFC, IDS, ISO 16739/29481), giving readers
  transferable concepts rather than tool-specific recipes.

---

## What is the honest novelty of this work?

The novelty is **not** a new ML algorithm or a record-breaking accuracy. The
honest contribution is the **transformation of standard concrete ML predictions
into an OpenBIM-ready Concrete Performance Passport** that:

1. binds prediction + uncertainty + explanation to an **element-level** record;
2. fuses **quality, durability, and sustainability** with an explicit **QA/QC
   decision** (the dominant prior work treats these separately, and passports
   treat them as reuse inventories);
3. provides a concrete **IFC mapping + a proposed `Pset_ConcretePerformancePassport`
   + an IDS-ready requirement matrix**, making the data verifiable in
   vendor-neutral openBIM workflows.

This is a *data-management and interoperability* contribution that operationalises
existing ML and standards, demonstrated reproducibly — appropriate scope for a
book chapter, with novelty stated without overclaiming.



---

# UPDATE (2025–2026 deep review)

> This section supersedes/strengthens the summary above following the rigorous
> 2025–2026 source-quality audit (`source_quality_audit.md`). It draws on the
> expanded set in `literature_matrix_updated.csv` (41 curated entries, ≥15 of
> them 2025–2026). Citation keys below refer to that updated matrix. Preprints
> and official documentation are flagged.

## What changed and why
The first pass was already fairly recent (≈46% from 2025–2026) but had coverage
gaps. This update adds: an **AI-applied-to-passports** systematic review
(`mdpi2026aipassport`, the closest combined prior art); a **concrete-specific
Digital Product Passport** (`plos2025concretedpp`); the **EU CPR DPP** regulatory
driver (`eu2025cprdpp`); an **applied openBIM IDS framework for carbon**
(`mdpi2025idscarbon`); an **IFC/BIM data-readiness-for-AI** review
(`mdpi2024ifcaiready`); an **open-standards (IFC/COBie/IDS/bSDD/LOIN)** review
(`mdpi2025bimfm`); a **BIM↔LCA AI matching tool** (`springer2025aibimlca`);
2026 **strength reviews/UQ** (`springer2026hpcreview`, `fbuil2026hetero`,
`mdpi2026uq`); and a peer-reviewed **DT-for-strength** anchor
(`screp2025dtstrength`).

## State of the art by stream (current)
- **ML for concrete (A):** accuracy is largely solved; 2025–2026 work emphasises
  **interpretability and uncertainty** (`mdpi2025xmlconcrete`, `mdpi2026uq`,
  `uncertaintygwp2025`). The open problem is *use*, not accuracy.
- **Durability (A):** real but **data-limited/heterogeneous**
  (`rilem2025durability`, `springer2025durabilitylca`) → optional, flagged block.
- **BIM/OpenBIM data management (B):** standards + **data-readiness-for-AI** are
  now explicit (`mdpi2024ifcaiready`, `mdpi2025bimfm`); QA stays
  inspection/document-centric (`mdpi2025qualisite`, `asce2025qms`).
- **BIM-LCA/EPD (D):** automation **emerging but early** (`springer2025aibimlca`);
  EPD-in-IFC **limited** (`mdpi2025epdifc`); EPD **data quality** matters
  (`ijlca2026dataquality`); public data/factors enable transparent benchmarking
  (`broyles2024epd`, `hammond2008ice`).
- **Material/Digital product passports (C):** going **digital and
  concrete-aware** but **reuse/EOL-centric** (`mdpi2026mppris`,
  `plos2025concretedpp`, `mdpi2026aipassport`), with **regulatory momentum**
  (`eu2025cprdpp`).
- **Construction DT QA/QC (E):** element-level **readiness decisions** emerging
  (`dt2026qaframework` preprint; `screp2025dtstrength`) but **not OpenBIM/IDS-
  bound**.
- **IDS (F):** **v1.0 final** and **applied to domain requirements**
  (`bsi_ids`, `mdpi2025idscarbon`).

## The integrated gap (sharpened)
No 2025–2026 source delivers, in one **element-level, OpenBIM-ready, IDS-checkable**
record: predicted strength **+ uncertainty/risk + explanation**, an **optional
durability** indicator, a **carbon class + EPD percentile**, and an explicit
**QA/QC decision**, mapped to IFC via a proposed `Pset_ConcretePerformancePassport`.
Adjacent works advance each piece; **the integration is the contribution.**

## Honest novelty (current wording)
The contribution is a **data-management and interoperability framework** that
**operationalises** concrete ML predictions, EPD-based carbon benchmarks, and
optional durability indicators into **OpenBIM-ready Concrete Performance
Passports** for element-level quality, durability, and sustainability decision
support — **not** a new ML algorithm. See `novelty_positioning.md`.

## Suitability for a 2026 Springer book chapter
A Springer editorial collection on **AI applications for concrete and concrete
structures** is active (`springer2025aicollection`), confirming demand. The
chapter's **integrative, standards-anchored, fully-reproducible-on-public-data**
character matches the expected depth of a practical book chapter (concepts,
models, applications) without overclaiming primacy.
