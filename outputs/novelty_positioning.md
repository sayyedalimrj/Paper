# Novelty Positioning

**Chapter:** AI-Enabled Concrete Performance Passports for OpenBIM

Grounded in `literature_matrix_updated.csv` and
`recent_literature_update_2025_2026.md`. Citation keys refer to the updated
matrix.

---

## 1. What exactly is new here?
A **concrete-specific, element-level, OpenBIM-ready data-management framework**
that **operationalises** existing ML and sustainability outputs into a single
verifiable record — the **Concrete Performance Passport** — which:
1. binds **predicted strength + uncertainty/risk + explanation (SHAP)** to a
   structural element;
2. attaches an **optional, provenance-flagged durability** indicator;
3. attaches an **EPD-based carbon class + benchmark percentile**;
4. emits an explicit **QA/QC decision** (Accept / Review / Hold / Retest /
   Missing-or-insufficient); and
5. maps to **IFC** (`IfcMaterial`, concrete element subtypes) via a proposed
   **`Pset_ConcretePerformancePassport`**, with an **IDS-ready requirement
   matrix** so delivered models can be **automatically checked**.

The novelty is the **integration + standardisation + checkability**, not any
single component.

## 2. What is not new?
- ML prediction of concrete strength/durability (`yeh1998`,
  `springer2026hpcreview`, `rilem2025durability`).
- SHAP/interpretability for concrete ML (`mdpi2025xmlconcrete`).
- Embodied-carbon/EPD benchmarking (`broyles2024epd`, `hammond2008ice`).
- The material/digital product passport concept (`honic2019mp`,
  `mdpi2026mppris`, `plos2025concretedpp`).
- IFC, the IDS standard, and BIM-based QA/QC (`bsi_ifcmaterial`, `bsi_ids`,
  `mdpi2025qualisite`).
- Applying AI to passports in general (`mdpi2026aipassport`).

## 3. Which previous works are closest?
- **`mdpi2026aipassport`** (AI applied to material/digital product passports) —
  closest *conceptually*, but broad and **reuse/circularity-oriented**, not a
  concrete performance/QA instantiation.
- **`plos2025concretedpp`** (concrete DPP) — closest on *concrete passports*, but
  **reuse/recycling lifecycle** focus, not in-construction performance/QA.
- **`dt2026qaframework`** (construction-phase QA digital twin, preprint) —
  closest on *element-level QA decisions*, but **not expressed in OpenBIM
  IFC/IDS** (not vendor-neutral or auto-checkable).
- **`mdpi2025idscarbon`** (openBIM IDS for operational carbon) — closest on
  *applied IDS for a domain*, but **carbon-only**, not quality+durability+QA.

Our work sits at the **intersection** none of these occupies.

## 4. How is this different from ML concrete-prediction studies?
They optimise accuracy and stop at a number/plot (`fbuil2026hetero`,
`screp2026dlllm`). We treat the prediction as **one field** in a decision record:
element-bound, **risk-typed via uncertainty**, explained, and **interoperable**.

## 5. How is this different from BIM-QA/QC systems?
Those manage **inspections, checklists, and quality documents** linked to
elements (`mdpi2025qualisite`, `asce2025qms`). We add **predictive performance,
durability, and carbon** plus a **derived QA decision**, and we make the data
**IDS-checkable**.

## 6. How is this different from material/digital product passports?
MPs/DPPs inventory **what material is where for future reuse/recovery**
(`mdpi2026mppris`, `plos2025concretedpp`). We record **how the element is
expected to perform and whether it passes QA now**, fusing quality, durability,
and sustainability for the **construction/in-service** phase.

## 7. How is this different from BIM-LCA/EPD matching tools?
Matching tools link BIM elements to LCA/EPD datasets for **carbon accounting**
(`springer2025aibimlca`), and EPD-in-IFC remains limited (`mdpi2025epdifc`). We
use carbon as **one block** of a broader performance passport and connect it to
**quality/QA decisions**, not carbon reporting alone.

## 8. Why does the project matter in practice?
Today, the data needed to accept or hold a concrete element lives in **separate
silos**: the lab sheet, the mix design, an ML notebook, an LCA/EPD tool, the
inspection log, and the BIM model. The passport **consolidates** these into one
structured, auditable, vendor-neutral record that travels with the element and
can be **validated automatically** against agreed requirements.

## 9. What problem does it solve, and for whom?
- **Concrete QA/QC teams:** an explicit, explainable **Accept/Review/Hold/Retest**
  decision per element, with uncertainty and missing-data handling.
- **Site/contractor teams:** earlier, traceable **readiness** information
  (e.g., strength sufficiency) tied to the element, reducing rework and delays.
- **BIM managers:** a defined **Pset + IDS requirement matrix** so performance
  data is delivered and **checkable**, not ad hoc.
- **Sustainability leads:** a **carbon class + benchmark percentile** on the same
  record as quality — enabling joint quality–carbon decisions.

## 10. What should we avoid claiming?
- Not a **new/state-of-the-art ML algorithm** or accuracy record.
- Not a **validated durability or service-life prediction**.
- Not **verified, product-specific EPD/LCA** results (we use public benchmarks
  and transparent factors).
- Not a **finished, certified IFC/IDS implementation** or commercial BIM
  integration.
- Not **"first ever"** anything — adjacent work exists; we claim a **specific,
  integrative, reproducible instantiation**, not primacy.
- The passport is **decision support**, not a replacement for testing, codes, or
  engineering judgement.

---

## Final novelty statement (refined)
> **The novelty is not a new ML algorithm. It is a data-management and
> interoperability framework that operationalises concrete ML predictions,
> EPD-based carbon benchmarks, and optional durability indicators into
> OpenBIM-ready Concrete Performance Passports for element-level quality,
> durability, and sustainability decision support — bundling prediction,
> uncertainty/risk, explanation, carbon class, and an explicit QA/QC decision,
> mapped to IFC via a proposed `Pset_ConcretePerformancePassport` and made
> machine-checkable through an IDS-ready requirement matrix, demonstrated
> reproducibly on public data.**
