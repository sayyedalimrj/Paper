# AI-Enabled Concrete Performance Passports for OpenBIM

**Machine Learning–Based Quality, Durability, and Sustainability Data Management for Concrete Structures**

This repository accompanies a Springer-style book chapter for the edited volume
*"Artificial Intelligence in Concrete Structures and Technologies: Concepts, Models, and Applications."*

---

## Current status (research-workflow draft)

- The **scientific framing, literature review (2025–2026 updated), data-management
  schema, OpenBIM/IDS mapping, chapter draft, and source code** are substantially
  developed and committed.
- **Computed artefacts** (trained model `.pkl`, real passport demonstration
  records, figures, model metrics) are **pending one offline regeneration run**.
  They were not generated in the latest pass because the full pipeline and the
  lightweight finalizer exceeded interactive execution constraints (hung). This is
  documented honestly in `outputs/final_report.md`,
  `outputs/scientific_acceptance_checklist.md`, and `outputs/test_report.md`.
- **No experimental results are claimed** until the offline finalizer and offline
  tests are run. No metrics or passport records are fabricated.

### Reproduce computed artefacts (offline, one command)
```bash
pip install -r requirements.txt
USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs   # cached data only; no downloads, no SHAP, no CV
USE_CACHED_ONLY=1 pytest -q                                    # offline sanity tests
```
> Do **not** run `python -m src.pipeline` in constrained/interactive environments;
> use the lightweight finalizer (`src/finalize_lightweight_outputs.py`) instead.

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
│   ├── 01_literature_and_dataset_inventory.ipynb
│   ├── 02_strength_model_and_passport_generation.ipynb
│   └── 03_carbon_and_openbim_mapping.ipynb
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

### Google Colab (primary path)
Open the notebooks in order. Each notebook installs its own dependencies,
downloads/loads data, runs end-to-end, and writes artefacts to `outputs/`.

1. `notebooks/01_literature_and_dataset_inventory.ipynb`
2. `notebooks/02_strength_model_and_passport_generation.ipynb`
3. `notebooks/03_carbon_and_openbim_mapping.ipynb`

### Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.config            # create output dirs
python -m src.data_download     # fetch public datasets
python -m src.train_strength_model
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
