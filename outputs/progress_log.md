# Progress Log — AI-Enabled Concrete Performance Passports for OpenBIM

This log is the durable, restartable record of the project. Each phase appends a
timestamped, structured entry (completed tasks, files, decisions, problems, next
actions). If context is lost, resume from the most recent entry plus the saved
files in `outputs/`.

---

### Phase 0 — Project setup (initial)

- **Completed:**
  - Inspected repository (was empty except `.git`).
  - Confirmed sandbox: Python 3.11 available, network mode OPEN_INTERNET.
  - Created full directory structure (`data/`, `notebooks/`, `src/`, `outputs/`, `tests/`).
  - Verified key public dataset provenance via web search (UCI Concrete Strength = Yeh 1998; NRMCA Industry-Average EPD for carbon benchmarks).
- **Files created/modified:**
  - `requirements.txt`
  - `README.md`
  - `src/config.py` (paths, dataset registry, seeds, schema)
  - `src/utils.py` (logging, seeding, metrics, progress-log appender)
  - `outputs/progress_log.md` (this file)
  - directory `.gitkeep` placeholders
- **Key decisions:**
  - Primary strength dataset = **UCI Concrete Compressive Strength** (Yeh, 1998), 1030 rows, 8 features (public, CC BY 4.0). Mirror via OpenML/sklearn if UCI host fails.
  - Carbon benchmarks anchored to **public NRMCA Industry-Average EPD** + **ICE database**; no fabricated values.
  - Durability modelling treated as *optional with fallback* due to scarcity of clean public CSVs; passport will mark durability "not assessed" rather than invent data.
  - OpenBIM mapping will use real IFC concepts (`IfcMaterial`, `Pset_MaterialConcrete`) + a proposed custom `Pset_ConcretePerformancePassport`; IDS emitted as conceptual XML if `ifcopenshell` is unavailable.
- **Problems encountered:**
  - None blocking. `ifcopenshell` may not pip-install cleanly in all environments → conceptual-mapping fallback planned.
- **Next actions:**
  - Implement `src/` modules (data_download, data_cleaning, train_strength_model, explainability, passport_schema, generate_passports, ifc_mapping).
  - Build the three Colab notebooks.
  - Train strength model, generate passports, produce figures/tables.
  - Draft the chapter into `outputs/chapter/`.


---

### Phase 0b — Data layer implemented & verified (same session)

- **Completed:**
  - Implemented and **verified** `src/data_download.py`: successfully downloaded the real UCI Concrete dataset from the UCI archive (`Concrete_Data.xls`, 124,928 bytes → 1030 rows × 9 cols) and wrote `data/raw/concrete_strength_raw.csv` + `data/raw/provenance.json`.
  - Implemented and **verified** `src/data_cleaning.py`: produced `data/processed/concrete_strength_clean.csv` (1030 rows × 13 cols) with engineered features (total_binder, water_cement_ratio, water_binder_ratio, scm_fraction).
  - Created documented Phase-2/3/4/5 stubs: `train_strength_model.py`, `train_durability_model.py`, `train_carbon_model.py`, `explainability.py`, `passport_schema.py`, `generate_passports.py`, `ifc_mapping.py`.
  - Created valid placeholder notebooks (01, 02, 03) with title + "what this produces" cells.
  - Added `.gitignore`, `src/__init__.py`, `outputs/execution_plan.md`.
- **Files created/modified:** `src/data_download.py`, `src/data_cleaning.py`, `src/__init__.py`, `src/train_strength_model.py`, `src/train_durability_model.py`, `src/train_carbon_model.py`, `src/explainability.py`, `src/passport_schema.py`, `src/generate_passports.py`, `src/ifc_mapping.py`, `notebooks/01..03.ipynb`, `.gitignore`, `outputs/execution_plan.md`, `data/raw/*`, `data/processed/*`.
- **Key decisions:**
  - Verified the data pipeline early so downstream phases start from a known-good processed CSV.
  - Engineered features chosen for both model signal and passport interpretability (w/c, w/cm ratios are standard mix-design indicators).
- **Problems encountered:** Sandbox uses pyenv; set global to 3.11.15 and installed core deps. No blockers.
- **Next actions:** Phase 2 — implement `train_strength_model.py` (baseline + gradient boosting, CV, hold-out metrics, figures) and `explainability.py`. Await next prompt or continue per plan.


---

### Phase 1 — Literature review + 2025–2026 deep update & source-quality audit

- **What I searched (web):** 2025–2026 ML concrete strength/durability reviews;
  explainable ML + uncertainty quantification; multi-output concrete ML; BIM/IFC
  data-readiness-for-AI; open standards (IFC/COBie/IDS/bSDD/LOIN); applied openBIM
  IDS for carbon; BIM-LCA/EPD interoperability + AI matching tools; material
  passports (PRISMA) + AI-applied-to-passports + concrete DPP + EU CPR DPP;
  construction-phase digital-twin QA/QC + early-age strength; Springer
  AI-in-concrete book scope; UCI / Mendeley EPD / SCM-RAC / buildingSMART /
  ICE dataset sources.
- **First-pass result:** 35 sources (`literature_matrix.csv`), 16 from 2025–2026.
  Audited in `source_quality_audit.md` (counts: 16 = 2025–2026; 11 = 2023–2024;
  8 older foundational). Gaps found: DPP/regulatory, concrete DPP,
  AI-applied-to-passports, applied IDS, IFC-data-readiness, UQ-for-strength,
  book-scope.
- **Update result:** new curated matrix `literature_matrix_updated.csv` with 41
  entries and richer columns (BIM/ML/data-management relevance, how-it-supports,
  how-we-differ, confidence). **≥15 entries are 2025–2026**; ≥5 BIM/OpenBIM/IFC/
  IDS; ≥5 ML-for-concrete; ≥3 BIM-LCA/EPD; ≥3 material/digital product passports;
  ≥2 construction DT/QA. Standards (IfcMaterial, concrete Psets, IDS, IDM) and
  datasets (UCI, Mendeley EPD, ICE, SCM-RAC) included.
- **New 2025–2026 sources added (highlights):** `mdpi2026aipassport` (AI+passports
  review — closest prior art), `plos2025concretedpp` (concrete DPP),
  `eu2025cprdpp` (EU CPR DPP, official), `mdpi2025idscarbon` (applied openBIM IDS
  for carbon), `mdpi2024ifcaiready` (IFC data-readiness-for-AI),
  `mdpi2025bimfm` (open-standards review), `springer2025aibimlca` (BIM↔LCA AI
  matching), `springer2026hpcreview`/`fbuil2026hetero`/`screp2026dlllm` (strength),
  `mdpi2026uq` (UQ), `screp2025dtstrength` (DT-for-strength),
  `springer2025durabilitylca` (durability+AI+LCA), `mdpi2026mppris` (PRISMA MP).
- **Files created:** `outputs/source_quality_audit.md`,
  `outputs/literature_matrix_updated.csv`,
  `outputs/recent_literature_update_2025_2026.md`,
  `outputs/novelty_positioning.md`, `outputs/chapter_evidence_map.md`.
- **Files updated:** `outputs/literature_summary.md` (appended 2025–2026 update),
  `outputs/research_gap_and_contributions.md` (appended 2025–2026 update),
  `outputs/progress_log.md` (this entry). Original `literature_matrix.csv`
  preserved unchanged.
- **Final recommended chapter framing:** *"The novelty is not a new ML algorithm;
  it is a data-management and interoperability framework that operationalises
  concrete ML predictions, EPD-based carbon benchmarks, and optional durability
  indicators into OpenBIM-ready Concrete Performance Passports for element-level
  quality, durability, and sustainability decision support — bundling prediction,
  uncertainty/risk, explanation, carbon class, and an explicit QA/QC decision,
  mapped to IFC via a proposed Pset_ConcretePerformancePassport and made
  machine-checkable through an IDS-ready requirement matrix, demonstrated
  reproducibly on public data."*
- **Limitations / weak spots remaining:** closest QA prior art is a **preprint**
  (`dt2026qaframework`); some author fields remain `(see DOI/URL)` where author
  lists were not reliably confirmed (completeness, not fabrication); a few items
  use ResearchGate links (`rilem2024carbonation`); the SCM-RAC durability dataset
  licence needs confirmation before any redistribution.
- **Decision:** literature update complete and saved. **Cleared to proceed to the
  coding/modelling phase** (Phase 2 — strength model + explainability) next.
- **Next actions:** implement `src/train_strength_model.py` + `explainability.py`;
  begin passport schema (Phase 3).



---

### Phase 0 — Stop old runs & freeze old results (scientific hardening pass)

- **Old runs:** No background processes running (the previous `python -m src.pipeline` background start was cancelled before launch; an earlier foreground run timed out at 120s and did NOT complete).
- **Old results superseded:** Any earlier partial pipeline/test results are marked **superseded** — files will change during this scientific-hardening pass, so prior results are invalid as final.
- **Final tests postponed:** Lightweight OFFLINE tests will be run only at the very end (Phase J), using cached/local data and tiny fixtures — no dataset downloads.
- **Caches available (offline regeneration possible):** `data/raw/concrete_strength_raw.csv`, `data/processed/concrete_strength_clean.csv`, `data/external/concrete_epd_raw.csv` (81 MB, already downloaded). Regeneration this pass uses these caches only.
- **Robustness decisions:** reduce CV folds, default to permutation/impurity importance instead of SHAP, fewer optional models, `USE_CACHED_ONLY` offline mode for data loaders, no optional IFC extraction blocking.
- **Existing outputs at start of pass:** only `outputs/tables/dataset_summary.csv`; no models/figures/passports/chapter yet (pipeline had not completed).



---

### Phase 0b — Full pipeline ABANDONED; switching to lightweight finalizer

- **Process check:** `ps -eo pid,etime,command | grep -E "src.pipeline|pytest|shap|cross_val|jupyter"` returned **no matching processes** (the backgrounded `python -m src.pipeline` was cancelled before launch; the earlier foreground attempt timed out at 120s and was not completed).
- **Decision:** `python -m src.pipeline` is **marked unsafe for this environment** and is **abandoned**. It will NOT be run again. Any previous pipeline/test result is **superseded**.
- **New approach:** all final outputs are regenerated by a single lightweight, offline, targeted script `src/finalize_lightweight_outputs.py` (no downloads, no SHAP, no cross-validation, no heavy models; target < 2 minutes).
- **Final tests:** postponed to the very end (Phase J), offline only, using cached/local data + tiny fixtures.
