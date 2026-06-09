# Chapter Evidence Map

Maps each planned chapter claim to supporting sources, with an honest strength-of-
evidence rating. Citation keys refer to `literature_matrix_updated.csv`.
Strength scale: **Strong** (multiple peer-reviewed/standard sources),
**Moderate** (one solid source or reviews), **Indicative** (preprint/emerging or
single study). Preprints and official docs are flagged in the matrix.

| # | Chapter claim | Supporting sources | Strength of evidence | Notes |
|---|---|---|---|---|
| 1 | ML is widely and successfully used for concrete property (esp. compressive strength) prediction. | `yeh1998`, `springer2026hpcreview`, `fbuil2026hetero`, `screp2026dlllm`, `springer2024compare`, `fmats2025hpc` | Strong | Mature field; ensembles/DL with R²>0.9 common. |
| 2 | ML for durability exists but is data-limited and generalises poorly. | `rilem2025durability`, `springer2025durabilitylca`, `rilem2024carbonation`, `prayogo2025scmrac` | Strong | RILEM TC review is authoritative; supports optional/flagged durability. |
| 3 | Interpretability (SHAP) and uncertainty quantification are increasingly standard in concrete ML. | `mdpi2025xmlconcrete`, `screp2025multitask`, `mdpi2026uq`, `uncertaintygwp2025` | Strong | Justifies embedding explanation + risk band in the passport. |
| 4 | ML outputs usually stop at a metric/plot and are not integrated into BIM-based data management. | `mdpi2024ifcaiready`, `mdpi2026aipassport`, `springer2026hpcreview` | Strong | Data-readiness review explicitly frames the integration gap. |
| 5 | BIM-QA/QC systems exist but focus on inspection/checklist/document workflows. | `mdpi2025qualisite`, `asce2025qms` | Moderate | Recent prototypes; inspection/document-centric. |
| 6 | Material/digital product passports mostly focus on circularity, reuse, and end-of-life. | `mdpi2026mppris`, `asce2024dimmp`, `plos2025concretedpp`, `honic2019mp` | Strong | PRISMA review + concrete DPP confirm reuse/EOL emphasis. |
| 7 | AI is now being applied to passports, but not as a concrete performance/QA instantiation. | `mdpi2026aipassport` | Moderate | Closest combined prior art; broad, reuse-oriented. |
| 8 | Digital product passports are gaining regulatory momentum (EU CPR). | `eu2025cprdpp` | Moderate | Official EU feasibility study (policy-level). |
| 9 | BIM-LCA/EPD integration remains challenged by interoperability and data mapping. | `mdpi2025epdifc`, `mdpi2026bimlca`, `ijlca2026dataquality` | Strong | EPD-in-IFC limits + data-quality effects on ML. |
| 10 | AI-based BIM↔LCA automation is emerging but early-stage and matching-focused. | `springer2025aibimlca` | Moderate | Nuances the "all manual" claim; design-phase, matching only. |
| 11 | Public EPD data and open carbon factors enable transparent benchmarking. | `broyles2024epd`, `hammond2008ice` | Strong | Dataset (tens of thousands of EPDs) + ICE factors. |
| 12 | IFC provides standard structures for materials/concrete elements, but not for ML/uncertainty/carbon-class/QA. | `bsi_ifcmaterial`, `bsi_psetconcrete`, `mdpi2025epdifc` | Strong | Motivates a custom `Pset_ConcretePerformancePassport`. |
| 13 | IFC/IDS provide a formal route for alphanumeric information requirements and automatic checking. | `bsi_ids`, `bsi_idm`, `mdpi2025bimfm` | Strong | IDS v1.0 final standard + open-standards review. |
| 14 | IDS can carry domain (e.g., sustainability) information requirements in practice. | `mdpi2025idscarbon` | Moderate | Applied openBIM IDS framework for operational carbon. |
| 15 | Element-level QA decision support (release/hold/retest) is emerging via construction digital twins. | `dt2026qaframework`, `screp2025dtstrength`, `screp2025earlyage`, `astm_c1074` | Moderate | Closest QA prior art is a preprint; not standards-bound. |
| 16 | Early-age strength estimation underpins construction-phase release decisions. | `astm_c1074`, `screp2025earlyage` | Strong | Standard practice + recent ML. |
| 17 | A Concrete Performance Passport can bridge ML prediction and project-level decision records, validatable in OpenBIM. | Synthesis: `mdpi2026aipassport` + `dt2026qaframework` + `mdpi2025idscarbon` + `bsi_ids` + `mdpi2025epdifc` | Moderate (synthesis) | No single source integrates all blocks — this is our contribution, argued from adjacent evidence. |
| 18 | The novelty is integration/operationalisation, not a new ML algorithm. | Negative-space argument across rows 1–17 | Moderate | Defensible positioning; avoid "first ever." |

## How to use this map when drafting
- Each Introduction/Related-Work paragraph should cite from the relevant row(s).
- Where strength is **Moderate/Indicative**, hedge language accordingly
  ("emerging", "recent prototypes", "a preprint reports").
- Row 17 is the **gap/contribution hinge** — present it as a synthesis of
  adjacent evidence, explicitly noting that no prior source integrates all blocks.
