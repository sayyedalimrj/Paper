# Recent Literature Update (2025–2026)

**Chapter:** AI-Enabled Concrete Performance Passports for OpenBIM — Machine
Learning–Based Quality, Durability, and Sustainability Data Management for
Concrete Structures

Companion to `literature_matrix_updated.csv` and `source_quality_audit.md`.
Citation keys (e.g., `mdpi2026aipassport`) refer to that matrix. Preprints and
official documentation are marked as such. No citations or DOIs were fabricated;
MDPI DOIs are derived deterministically from the publisher's URL scheme.

> Compliance note: all source content is paraphrased/summarised.

---

## 1. Why an updated literature review was needed
The chapter targets a **2026 Springer Nature** edited volume, so the review must
reflect **2025–2026** scholarship rather than treating 2024 as a cutoff. The
first pass was already 46% from 2025–2026 (see audit), but had **coverage gaps**:
no Digital Product Passport (DPP) or EU regulatory driver, no concrete-specific
DPP, no *AI-applied-to-passports* review (the closest combined prior art), only
the IDS standard page (no applied IDS study), and no BIM↔LCA automation example.
This update closes those gaps and refreshes each stream with current sources.

## 2. Recent ML advances in concrete property prediction
2025–2026 work confirms that strength prediction is mature and converging on
**ensemble/boosted-tree and deep-learning** models with **interpretability** as
standard. A 2026 review consolidates SVM/DT/RF/GB/XGB/ANN for HPC strength
(`springer2026hpcreview`); **heterogeneity-aware stacked ensembles** improve
robustness across pooled datasets (1525 mixes, `fbuil2026hetero`); and
frontier studies combine **optimized deep learning with LLM assistance**
(`screp2026dlllm`). Crucially for our framing, **uncertainty quantification** is
now appearing for strength (`mdpi2026uq`) and jointly with carbon
(`uncertaintygwp2025`). **Takeaway:** accuracy is largely solved; the open
problem is what to *do* with the prediction — exactly the data-management gap we
target.

## 3. Recent durability and multi-property concrete ML work
The **RILEM TC 315-DCS** review (`rilem2025durability`) authoritatively maps
durability ML (carbonation, chloride, sulfate, frost, shrinkage, corrosion) and
flags **data scarcity, heterogeneity, and weak generalisation**. A 2025 Springer
review integrates **durability modelling with AI and LCA** for service-life-aware
carbon (`springer2025durabilitylca`). Multi-output frameworks predict several
mechanical/durability targets jointly (`prayogo2025scmrac`,
`screp2025multitask`). **Takeaway:** durability prediction is real but
data-limited — supporting our decision to treat durability as an *optional,
provenance-flagged* passport block rather than fabricating values.

## 4. Recent BIM/OpenBIM data management work
Two recent reviews are pivotal. **"BIM and IFC data readiness for AI"**
(`mdpi2024ifcaiready`) argues IFC/BIM data must be deliberately structured for AI
to be usable — directly supporting our claim that ML outputs need a standardised
home. **"BIM-FM interoperability through open standards"** (`mdpi2025bimfm`)
synthesises the modern openBIM toolset (IFC, COBie, **IDS v1.0**, **bSDD**,
**ISO 7817-1 Level of Information Need**). BIM-based QA/QC remains
**inspection/document-centric** (`mdpi2025qualisite`, `asce2025qms`).
**Takeaway:** the standards and the data-readiness arguments now exist; what is
missing is a concrete-performance instantiation.

## 5. Recent BIM/AI/LCA/EPD integration work
A 2025 study presents an **open-access AI tool that auto-matches BIM elements to
LCA datasets** (`springer2025aibimlca`) — evidence that automation is *emerging*
(nuancing the older "all manual/spreadsheet" claim) but still **early-stage and
design-phase**, focused on *matching*, not decision-ready records. In parallel,
**EPD data is shown to be hard to represent in IFC** (`mdpi2025epdifc`), BIM↔LCA
interoperability remains challenged (`mdpi2026bimlca`), and **EPD data quality
measurably degrades ML reliability** (`ijlca2026dataquality`). Large public EPD
data (`broyles2024epd`) and open carbon factors (`hammond2008ice`) make
transparent benchmarking feasible. **Takeaway:** carbon data and matching exist,
but are not packaged per element with quality and QA.

## 6. Recent material passport and digital product passport work
This is the fastest-moving and most directly relevant stream. A 2026 **PRISMA
review of material passports** (46 studies) confirms the **circularity/reuse**
framing dominates (`mdpi2026mppris`). A 2026 **critical systematic review of AI
applications to material and digital product passports** (`mdpi2026aipassport`)
is the **closest combined prior art** to our idea (AI + passports) — yet it is
broad and not concrete-performance specific. A 2025 **concrete-specific Digital
Product Passport** for recycled/natural aggregate concrete elements
(`plos2025concretedpp`) shows passports reaching concrete, but with a
**reuse/recycling lifecycle** emphasis. The **EU CPR Digital Product Passport
feasibility study** (`eu2025cprdpp`, official) signals strong regulatory momentum.
**Takeaway:** passports are going digital and concrete-aware, but remain
reuse/EOL-centric; **performance/quality/durability/QA during construction and
service is the open niche.**

## 7. Recent construction digital twin and QA/QC decision-support work
A construction-phase **digital twin framework** links inspection, production,
early-age sensing, and predictive strength to elements for **readiness-based
(release/hold/retest-style) decisions** (`dt2026qaframework`, preprint) — the
closest QA/QC prior art. A peer-reviewed 2025 **DT-for-strength** study
benchmarks a DNN twin against classical ML on public data (`screp2025dtstrength`).
Early-age strength prediction (`screp2025earlyage`; ASTM C1074 maturity,
`astm_c1074`) underpins construction-phase decisions. **Takeaway:** element-level
QA decision support is emerging but **not expressed through OpenBIM IFC/IDS**, so
it is not vendor-neutral or automatically checkable.

## 8. Recent IDS/OpenBIM information-requirement developments
IDS reached **v1.0 final standard** (`bsi_ids`) and is being applied: a 2025
study develops an **openBIM IDS framework for operational carbon impact
assessment** (`mdpi2025idscarbon`) — direct precedent that **IDS can carry
domain (sustainability) requirements** beyond geometry. Open-standards reviews
position IDS alongside bSDD and LOIN (`mdpi2025bimfm`). **Takeaway:** IDS is now
a usable, applied mechanism for alphanumeric requirements — ready to host a
*concrete performance* requirement set.

## 9. What is still missing in the literature
Even in 2025–2026, no source provides **all** of the following in one,
element-level, OpenBIM-ready record:
- ML **predicted strength + uncertainty/risk + explanation**, *bound to an
  element*;
- an **optional durability** indicator with honest provenance;
- a **carbon class + EPD-based benchmark percentile**;
- an explicit **QA/QC decision** (Accept/Review/Hold/Retest/Missing); and
- a mapping to **IFC + a custom Pset + an IDS-checkable requirement matrix**.
AI+passport work (`mdpi2026aipassport`) and concrete DPPs (`plos2025concretedpp`)
are reuse-centric; QA digital twins (`dt2026qaframework`) are not standards-bound;
IDS-carbon work (`mdpi2025idscarbon`) covers carbon only. **The integration is
the gap.**

## 10. Why the Concrete Performance Passport framing is stronger than the alternatives
- **vs a simple ML strength-prediction chapter:** those stop at a metric
  (`yeh1998`, `springer2026hpcreview`, `fbuil2026hetero`). We make the prediction
  *actionable and interoperable* (element-bound, risk-typed, IFC/IDS-checkable).
- **vs a simple low-carbon benchmarking chapter:** carbon-only work
  (`springer2025lowcarbonreview`, `broyles2024epd`) ignores quality/QA. We fuse
  carbon **with** strength/durability and a decision.
- **vs a simple IFC-readiness chapter:** readiness reviews (`mdpi2024ifcaiready`,
  `mdpi2025epdifc`) diagnose gaps but do not deliver a concrete-performance
  schema/Pset/IDS. We deliver a worked instantiation.
- **vs a simple material-passport chapter:** MPs/DPPs (`mdpi2026mppris`,
  `plos2025concretedpp`, `mdpi2026aipassport`) target reuse/EOL. We target
  in-construction/in-service **performance, quality, durability, and
  sustainability** decision support.

## 11. Final refined research gap
There is **no standardised, element-level, OpenBIM-ready data carrier** that
**operationalises** concrete ML predictions (with uncertainty and explanation),
an optional durability indicator, and EPD-based carbon benchmarking into an
explicit **QA/QC decision**, mapped to **IFC** (via a proposed
`Pset_ConcretePerformancePassport`) and **validatable via buildingSMART IDS**.
Adjacent 2025–2026 work advances each piece (AI+passports, concrete DPPs, QA
digital twins, applied IDS-for-carbon) but **none integrates them** for
construction-/service-phase concrete performance.

## 12. Final refined contribution statement
> **The contribution is not a new ML algorithm.** It is a **data-management and
> interoperability framework** that operationalises concrete ML predictions,
> EPD-based carbon benchmarks, and optional durability indicators into
> **OpenBIM-ready Concrete Performance Passports** — element-level records that
> bundle predicted performance, uncertainty/risk, explanation, carbon class, and
> an explicit QA/QC decision, mapped to IFC via a proposed
> `Pset_ConcretePerformancePassport` and made **machine-checkable through an
> IDS-ready requirement matrix** — demonstrated reproducibly on public data.
