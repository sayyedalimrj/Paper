# Source-Quality Audit of the Initial Literature Review

**Date:** 2026-06-09 · **Auditor pass:** rigorous update for a 2026 Springer
Nature book chapter.

This audit reviews the first-pass literature deliverables
(`literature_matrix.csv`, `literature_summary.md`,
`research_gap_and_contributions.md`, `dataset_inventory.md`) before the
2025–2026 update. The original matrix is preserved unchanged; the strengthened
set is in `literature_matrix_updated.csv`.

> No citations or DOIs were fabricated. Where the first pass used `(see DOI)` for
> authors, that is flagged below as a completeness weakness, not invented data.

---

## 1. How many sources were found in total (first pass)
**35** sources (`L01`–`L35`).

## 2. How many are from 2025–2026
**16** (≈46%).
- **2026:** 5 — `L19`, `L20`, `L23`, `L27`, `L28` (one is an arXiv preprint).
- **2025:** 11 — `L02`, `L05`, `L08`, `L09`, `L10`, `L14`, `L15`, `L22`, `L25`,
  `L26`, `L31`.

## 3. How many are from 2023–2024
**11**.
- **2024:** 10 — `L03`, `L04`, `L06`, `L11`, `L18`, `L21`, `L35`, plus standards
  pages accessed in 2024 (`L12`, `L13`, `L32`).
- **2023:** 1 — `L07`.

## 4. How many are older foundational sources
**8** — `L01` (1998, Yeh benchmark), `L16` (2022), `L17` (2019, Honic MP),
`L24` (2020), `L29` (2017, ASTM C1074), `L30` (2020), `L33` (2010, ISO 29481/IDM),
`L34` (2008, Hammond & Jones ICE).

**Verdict on recency:** the first pass was *already fairly recent* (46% from
2025–2026), so the issue is **not** that 2024 was treated as a cutoff. The real
weaknesses are **coverage gaps** and **citation completeness**, addressed below.

---

## 5. Which research areas are under-covered

| Area | Status in first pass | Gap |
|---|---|---|
| A. ML strength/durability | Well covered | Missing newest **2026** review(s) and **uncertainty-quantification** for strength specifically |
| B. BIM/OpenBIM/IFC QA/QC | Covered for QA/QC | Missing **IFC/BIM data-readiness-for-AI** and **open-standards (IDS/COBie/bSDD/LOIN)** synthesis |
| C. Material passports | Covered (reuse/EOL) | Missing **Digital Product Passport (DPP)**, **EU CPR/ESPR regulatory driver**, **concrete-specific DPP**, and **AI-applied-to-passports** |
| D. BIM-LCA/EPD | Covered | Missing **AI-driven BIM↔LCA matching tool** (shows automation is emerging) |
| E. Construction DT QA/QC | Thin (1 preprint + older) | Missing a **peer-reviewed 2025 DT-for-concrete-strength** anchor |
| F. IDS | Only the **standard page** | Missing an **applied IDS** paper (e.g., IDS for carbon/domain requirements) |
| G. Book-scope calibration | Absent | No reference to a Springer AI-in-concrete collection to calibrate depth |

## 6. Which sources are weak, generic, outdated, or not directly relevant
- **`L03` (ML+GUI, 2024):** generic; usability point can be made with one line —
  low unique value. *Demote.*
- **`L16` (broad BIM review, 2022):** generic and the oldest BIM-QA item;
  superseded by newer open-standards reviews. *Demote / replace.*
- **`L11` (RILEM TC 281-CCC) and `L24` (Obrecht et al. 2020):** cited via
  **ResearchGate** links rather than canonical DOIs — acceptable as evidence but
  weak as citations. *Upgrade link/keep as supporting.*
- **`L30` (formwork monitoring, 2020):** still useful but dated; pair with a
  newer DT anchor.

## 7. Which claims currently need stronger citations
1. *"ML outputs are not integrated into BIM data management."* → add **IFC/BIM
   data-readiness-for-AI review** and **AI-applied-to-passports review**.
2. *"Material passports stop at reuse/EOL."* → add **PRISMA MP review**,
   **concrete DPP study**, and **DPP regulatory driver (EU CPR)**.
3. *"IDS can carry domain information requirements."* → add an **applied openBIM
   IDS framework** (beyond the standard page).
4. *"BIM-LCA/EPD integration remains manual/immature."* → add the **2025
   AI-driven BIM↔LCA matching tool** (nuance: automation now emerging but
   early-stage and design-phase focused).
5. *"Strength predictions should carry uncertainty/risk."* → add a recent
   **uncertainty-quantification** strength study.

## 8. What must be updated before writing the book chapter
- [x] Add ≥10 new **2025–2026** sources, prioritising the gaps in §5.
- [x] Add ≥1 **applied IDS** source and ≥1 **DPP/regulatory** source.
- [x] Add a **concrete-specific DPP** source and an **AI-applied-to-passports** review (closest prior art).
- [x] Add **book-scope** calibration (Springer AI-in-concrete collection).
- [x] Produce `literature_matrix_updated.csv` with richer columns
  (BIM/ML/data-management relevance, how-it-supports, how-we-differ, confidence).
- [x] Strengthen and refresh `literature_summary.md` and
  `research_gap_and_contributions.md`.
- [x] Add `recent_literature_update_2025_2026.md`, `novelty_positioning.md`,
  `chapter_evidence_map.md`.

All items are completed in this update pass (see the new files).
