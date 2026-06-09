# Research Gap, Questions, Objectives, Contributions, and Scope

**Chapter:** AI-Enabled Concrete Performance Passports for OpenBIM — Machine
Learning–Based Quality, Durability, and Sustainability Data Management for
Concrete Structures

Grounded in `literature_matrix.csv` and `literature_summary.md`.

---

## 1. Research gap

Across the reviewed literature there is **no standardised, element-level,
OpenBIM-ready data carrier** that unifies:

- machine-learning **predicted performance** (compressive strength; optionally a
  durability indicator) with **prediction uncertainty / risk**;
- an **explanation** of the prediction (feature importance / SHAP);
- a **sustainability** assessment (embodied-carbon / GWP class and EPD-based
  benchmark percentile); and
- an explicit **QA/QC decision** (Accept / Review / Hold / Retest / Missing data),

mapped to **IFC** concepts and **verifiable via buildingSMART IDS**.

Concretely:
- **ML studies** stop at a metric and a plot; outputs are not element-bound,
  uncertainty-aware-in-decision, or interoperable (`yeh1998`, `fmats2025hpc`,
  `mdpi2025xmlconcrete`).
- **Material passports** are reuse/end-of-life inventories, not
  performance/quality/durability/sustainability records (`honic2019mp`,
  `asce2024dimmp`, `mdpi2026mp`).
- **BIM-QA/QC** systems remain document/inspection-centric (`mdpi2025qualisite`,
  `asce2025qms`).
- **BIM-LCA/EPD** integration is hampered by interoperability gaps and weak EPD
  representation in IFC (`obrecht2020bimlca`, `mdpi2025epdifc`,
  `ijlca2026dataquality`).
- **Construction-phase digital-twin QA** is emerging but not expressed through
  IFC/IDS standards (`dt2026qaframework`).

---

## 2. Research questions

- **RQ1.** What minimal, element-level information schema can carry concrete ML
  predictions together with uncertainty, explanation, carbon class, and a QA/QC
  decision?
- **RQ2.** How can this schema be mapped to existing IFC concepts
  (`IfcMaterial`, `Pset_MaterialConcrete`, element subtypes), and what custom
  property set (`Pset_ConcretePerformancePassport`) is needed for fields IFC does
  not natively cover?
- **RQ3.** How can the passport's information requirements be expressed as an
  **IDS-ready** requirement matrix so that delivered models can be checked
  automatically?
- **RQ4.** Can the full workflow be demonstrated **reproducibly on public data**
  (strength + EPD/carbon) using a transparent, explainable model and documented
  fallbacks?

---

## 3. Objectives

1. Train a reproducible, explainable **compressive-strength** model on the public
   UCI dataset, with hold-out + cross-validated metrics and an **uncertainty /
   risk** estimate.
2. Define a **Concrete Performance Passport schema** (six blocks: BIM/element,
   mix & test, ML outputs, sustainability/carbon, QA/QC decision, OpenBIM/IDS
   references) with provenance labels (dataset- / model- / demonstration-derived).
3. Derive a **carbon class and EPD-based benchmark percentile** from public EPD
   data and transparent ICE carbon factors (no fabricated values).
4. Produce an **IFC mapping**, a proposed **`Pset_ConcretePerformancePassport`**,
   and an **IDS-ready requirement matrix** (+ conceptual IDS XML).
5. Deliver everything as **runnable Colab notebooks** + scripts with saved
   artefacts.

---

## 4. Contributions

- **C1 — Concrete Performance Passport schema:** an element-level, six-block
  data model unifying quality, durability, sustainability, and QA/QC decision
  support (with explicit data-provenance flags).
- **C2 — OpenBIM mapping:** a field-by-field mapping of passport content to IFC
  concepts plus a proposed custom `Pset_ConcretePerformancePassport` for fields
  not covered by standard property sets (ML prediction, uncertainty, carbon
  class, QA decision).
- **C3 — IDS-ready requirement matrix:** machine-checkable information
  requirements for concrete performance data, enabling automated validation.
- **C4 — Reproducible demonstration:** an end-to-end, public-data, explainable
  pipeline (strength model -> uncertainty/risk -> SHAP -> carbon class -> QA
  decision -> passport -> IFC/IDS) runnable in Google Colab.

---

## 5. Scope

**In scope:** alphanumeric/tabular concrete data; compressive strength modelling;
optional durability indicator if a clean public dataset is available; embodied
carbon (cradle-to-gate, A1–A3 GWP) classification from public EPD/ICE data;
mapping to IFC + IDS; reproducible notebooks/scripts.

**Out of scope (explicitly):** image-based crack detection, 3D geometry, point
clouds, drone data, scan-to-BIM, and Revit-API/plugin development. The workflow
requires **no geometry, images, or proprietary BIM authoring**.

---

## 6. Limitations (honest)

- The strength model uses the standard UCI dataset (8 mix-design inputs); it does
  not include cement chemistry, aggregate gradation, or curing regime beyond age.
- **Durability** modelling is optional; public durability datasets are scarce and
  heterogeneous (`rilem2025durability`), so durability may be reported as
  "not assessed" rather than predicted.
- **Carbon** estimates use transparent published factors (ICE) and public EPD
  benchmarks; they are indicative class/percentile assignments, not plant- or
  product-specific verified EPDs.
- **BIM/element context** (element IDs, types, quantities) in the demonstration
  is synthetic and clearly labelled; it illustrates the schema, it is not a real
  project model.
- The IFC mapping and IDS matrix are **specification-level**; full IFC authoring
  and certified IDS validation against commercial tools are beyond the chapter.

---

## 7. What this chapter does NOT claim

- It does **not** claim a new or state-of-the-art ML algorithm or accuracy.
- It does **not** claim a validated durability or service-life prediction.
- It does **not** claim verified, product-specific EPD/LCA results.
- It does **not** claim a finished, certified IFC/IDS implementation or a
  commercial BIM integration.
- It does **not** claim to replace laboratory testing, codes, or professional
  engineering judgement; the passport is **decision support**, not a decision
  authority.



---

# UPDATE (2025–2026 deep review)

> Strengthened after the source-quality audit (`source_quality_audit.md`) and the
> 2025–2026 deep search. References use citation keys from
> `literature_matrix_updated.csv`.

## Refined research gap (current)
Across 2025–2026 literature, each component now exists in isolation — AI applied
to passports (`mdpi2026aipassport`), concrete Digital Product Passports
(`plos2025concretedpp`), construction-phase QA digital twins
(`dt2026qaframework`, preprint), applied openBIM IDS for carbon
(`mdpi2025idscarbon`), IFC/BIM data-readiness-for-AI (`mdpi2024ifcaiready`), and
EPD-in-IFC limitations (`mdpi2025epdifc`). **No source integrates them** into a
single **element-level, OpenBIM-ready, IDS-checkable** Concrete Performance
Passport that fuses predicted strength (+ uncertainty/risk + explanation),
optional durability, carbon class/percentile, and an explicit QA/QC decision.

## Refined contributions (current)
- **C1 — Concrete Performance Passport schema** (six provenance-flagged blocks)
  fusing quality, durability, sustainability, and QA/QC — distinct from
  reuse-centric MPs/DPPs (`mdpi2026mppris`, `plos2025concretedpp`).
- **C2 — OpenBIM mapping + `Pset_ConcretePerformancePassport`** for fields IFC
  does not natively cover (ML prediction, uncertainty, carbon class, QA decision),
  addressing documented EPD-in-IFC gaps (`mdpi2025epdifc`).
- **C3 — IDS-ready requirement matrix** for concrete performance data, extending
  applied IDS beyond carbon-only (`mdpi2025idscarbon`) to quality+durability+QA.
- **C4 — Reproducible, public-data demonstration** (strength → uncertainty/risk →
  SHAP → carbon class → QA decision → passport → IFC/IDS), aligned with the
  data-readiness-for-AI agenda (`mdpi2024ifcaiready`).

## Strengthened positioning vs alternatives
- Stronger than a **strength-prediction** chapter (which stops at accuracy:
  `springer2026hpcreview`, `fbuil2026hetero`).
- Stronger than a **low-carbon benchmarking** chapter (carbon-only:
  `springer2025lowcarbonreview`, `broyles2024epd`).
- Stronger than an **IFC-readiness** chapter (diagnostic only:
  `mdpi2024ifcaiready`, `mdpi2025epdifc`).
- Stronger than a **material-passport** chapter (reuse/EOL:
  `mdpi2026mppris`, `mdpi2026aipassport`).

## Additional limitations surfaced by the update
- The closest QA prior art (`dt2026qaframework`) is a **preprint**; we cite it as
  such and do not overstate consensus on construction-phase QA digital twins.
- AI BIM↔LCA automation exists but is **early-stage/design-phase**
  (`springer2025aibimlca`) — we avoid claiming mature interoperability.
- DPP **regulatory** frameworks (`eu2025cprdpp`) are evolving; we treat them as
  motivation, not a fixed technical target.

## What this chapter still does NOT claim (reaffirmed)
No new/SOTA ML algorithm; no validated durability/service-life prediction; no
verified product-specific EPD/LCA; no certified IFC/IDS implementation; no
"first ever" primacy. The passport is **decision support**, not a decision
authority.
