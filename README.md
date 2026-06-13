# AI-Enabled Concrete Performance Passports for OpenBIM

**Machine Learning–Based Quality, Durability, and Sustainability Data Management for Concrete Structures**

This repository accompanies a Springer-style book chapter for the edited volume
*"Artificial Intelligence in Concrete Structures and Technologies: Concepts, Models, and Applications."*

---

## Current status

- The **scientific framing, literature review (2025–2026 updated), data-management
  schema, OpenBIM/IDS mapping, chapter draft, and source code** are developed and
  committed.
- The **full pipeline now runs end-to-end** and regenerates every computed
  artefact: the trained model `.pkl`, model-comparison metrics, feature importance,
  the EPD-benchmarked carbon tables, the Concrete Performance Passports
  (CSV + JSON + one JSON per element), the OpenBIM/IDS artefacts, and all figures.
  On the UCI strength dataset the best model reaches **R² ≈ 0.92** on a hold-out
  split (XGBoost when available; otherwise ExtraTrees/RandomForest).
- A **single unified Google Colab notebook**
  (`notebooks/concrete_performance_passport_pipeline.ipynb`) runs the whole workflow,
  **saves all artefacts to Google Drive**, and is **checkpointed** so it can resume
  if the runtime disconnects.
- **No metrics or passport records are fabricated**; provenance and evidence levels
  (A–D) are recorded throughout.

### Reproduce computed artefacts
```bash
pip install -r requirements.txt
python -m src.pipeline      # full run (downloads public data, trains, builds passports)
pytest -q                   # sanity tests
```
Offline / cached-only variant (no network):
```bash
USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs
USE_CACHED_ONLY=1 pytest -q
```

### No-overclaim statement
No new ML algorithm, no full digital twin, no official IFC property set, no
legal/regulatory compliance, no validated durability solution, no real-project
validation, and no "first-ever" claim are made.

---

## 1. Core idea

Most machine-learning (ML) studies in concrete engineering stop at predicting a
single property — usually compressive strength, a durability indicator, or a
carbon-footprint number. This project goes one step further: it transforms ML
predictions into an **OpenBIM-ready "Concrete Performance Passport"** that
supports *element-level* data management and decision-making for concrete
structures.

The novelty is **not** a new ML algorithm. The contribution is the
**transformation of standard concrete ML predictions into OpenBIM-ready
performance passports** that bundle quality, durability, and sustainability
information together with QA/QC decision support and a mapping to IFC/IDS
concepts.

A **Concrete Performance Passport** organises, for each concrete element or mix
record:

1. **BIM / element information** — element ID, element type (beam, column,
   slab, wall, footing, pile, bridge deck, pier, …), required compressive
   strength, material name / concrete class, quantity/volume (when available).
2. **Concrete mix & test data** — cement, water, SCMs (fly ash, slag, silica
   fume), aggregates, superplasticiser/admixtures, age/curing time, measured or
   predicted properties.
3. **ML outputs** — predicted compressive strength, optional durability
   property, prediction uncertainty / risk category, feature-importance / SHAP
   explanation.
4. **Sustainability / carbon** — GWP / embodied-carbon benchmark (from public
   EPD data), carbon class (Low / Typical / High), EPD-based benchmark
   percentile where feasible.
5. **QA/QC decision support** — Accept / Review / Hold / Retest /
   Missing-or-insufficient data.
6. **OpenBIM / IDS-ready data management** — mapping of passport fields to IFC
   concepts (`IfcMaterial`, `Pset_MaterialConcrete`, …), a proposed custom
   `Pset_ConcretePerformancePassport`, and an IDS-ready requirement matrix.

> **Scope guardrails.** No images, point clouds, 3D geometry, scan-to-BIM, drone
> data, or Revit-API development. Public datasets only. No fabricated data or
> citations. No overclaimed novelty.

---

## 2. Repository structure

```
.
├── README.md
├── requirements.txt
├── data/
│   ├── raw/            # downloaded source datasets (not committed if large)
│   ├── processed/      # cleaned / feature-engineered tables
│   └── external/       # carbon benchmarks, EPD-derived reference values
├── notebooks/
│   └── concrete_performance_passport_pipeline.ipynb   # unified, Drive-backed, checkpointed
├── src/
│   ├── config.py             # paths, dataset registry, seeds
│   ├── data_download.py       # public dataset downloads with fallbacks
│   ├── data_cleaning.py       # schema normalisation, validation
│   ├── train_strength_model.py
│   ├── train_durability_model.py
│   ├── train_carbon_model.py
│   ├── explainability.py      # feature importance / SHAP (with fallback)
│   ├── passport_schema.py     # passport dataclass + JSON schema
│   ├── generate_passports.py  # builds passports from predictions
│   ├── ifc_mapping.py         # IFC / Pset / IDS mapping + XML emit
│   └── utils.py
├── outputs/
│   ├── figures/  tables/  models/  chapter/  passports/
│   ├── progress_log.md
│   └── execution_plan.md
└── tests/
```

---

## 3. Public datasets

| Dataset | Use | Source | Citation |
|---|---|---|---|
| **UCI Concrete Compressive Strength** (1030 rows, 8 features) | Strength model + passport demo | [UCI ML Repository](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength) (also on OpenML) | Yeh, I-C. (1998). *Cement and Concrete Research*, 28(12), 1797–1808. |
| **NRMCA Industry-Average EPD / regional GWP benchmarks** | Carbon class + benchmark percentile | [NRMCA EPD program](https://www.nrmca.org/association-resources/sustainability/environmental-product-declarations/) | NRMCA Industry-Average EPD (public report). |
| **ICE database (Inventory of Carbon & Energy)** | Material-level embodied-carbon factors | Circular Ecology (public, attribution required) | Hammond & Jones, ICE database. |

> Durability data with clean public CSVs is scarce. If a suitable public
> carbonation/chloride dataset cannot be obtained, the durability model is
> documented as a *fallback* (see `outputs/progress_log.md`) and the passport
> records durability as "not assessed" rather than fabricating values.

---

## 4. How to run

### Google Colab (primary path) — one unified notebook
Open **`notebooks/concrete_performance_passport_pipeline.ipynb`** in Colab and run
the cells top to bottom. The notebook:

1. **Mounts Google Drive** and creates a project folder
   (`MyDrive/ConcretePerformancePassport/` by default) that holds **all** `data/`
   and `outputs/`.
2. Clones the code, installs dependencies, and points the project root at Drive.
3. Runs every phase — data → strength model → explainability → carbon →
   passports → OpenBIM/IDS → figures — with a **checkpoint per phase**.
4. Verifies all artefacts and previews the key figures inline.

**Resume after a disconnect:** just re-run the notebook from the top. Each phase
checks a checkpoint file (`_checkpoints.json`) and the presence of its outputs on
Drive, and **skips work that is already complete**, so training continues where it
stopped. Use the reset helpers near the bottom to force a phase (or everything) to
re-run.

> Editable settings live in the second code cell: `PROJECT_NAME`, `REPO_BRANCH`,
> `N_PASSPORTS`, `USE_SHAP`, `FORCE_OFFLINE`.

### Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline          # full end-to-end run -> outputs/
# or run phase by phase:
python -m src.data_download
python -m src.train_strength_model
python -m src.train_carbon_model
python -m src.generate_passports
python -m src.ifc_mapping
```

---

## 5. Reproducibility

- Global random seed (`RANDOM_SEED = 42`) set via `src/utils.set_seed`.
- All artefacts are written to `outputs/`.
- Every phase appends a structured entry to `outputs/progress_log.md`.
- Datasets are public; provenance and licences are recorded in `src/config.py`.

---

## 6. Licence & attribution

Code is provided for research/educational use. Datasets retain their original
licences (UCI CC BY 4.0; ICE database requires attribution; NRMCA EPD reports
are publicly published). Citations are recorded in the chapter and in
`src/config.py`.
