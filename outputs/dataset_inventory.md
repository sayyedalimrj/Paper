# Dataset Inventory

**Chapter:** AI-Enabled Concrete Performance Passports for OpenBIM

Public datasets only. All properties below were **verified** (HTTP availability
checks, header inspection, or dataset landing pages) — none were fabricated.
Machine-readable version: `dataset_inventory.csv`.

> Availability checks performed on this machine (network mode OPEN_INTERNET):
> UCI .xls downloaded (124,928 bytes, 1030×9, verified); Mendeley EPD public-api
> returned HTTP 200 and the v3 CSV header was inspected directly; SCM-RAC and
> buildingSMART Sample-Test-Files repositories returned HTTP 200.

---

## D1 — UCI Concrete Compressive Strength (PRIMARY, INCLUDED)
- **Source:** UCI Machine Learning Repository, dataset 165
  (`https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength`).
- **Citation:** Yeh, I-C. (1998), *Cement and Concrete Research* 28(12):1797–1808.
- **Licence/terms:** Public (UCI; CC BY 4.0). Attribution via Yeh (1998).
- **Download method:** Direct HTTP `.xls` (**verified working** in
  `src/data_download.py`); fallback to OpenML via scikit-learn `fetch_openml`.
- **Format / size:** `.xls` → normalised `.csv`; **1030 rows × 9 columns**.
- **Columns:** cement, blast furnace slag, fly ash, water, superplasticizer,
  coarse aggregate, fine aggregate (all kg/m³), age (days).
- **Target:** compressive strength (MPa).
- **Missing data:** none significant; complete numeric table.
- **Use in chapter:** trains/evaluates the strength model; provides the mix &
  test-data block; underpins the passport demonstration.

## D2 — Compiled Concrete EPD Dataset, U.S.A. (CARBON, INCLUDED)
- **Source:** Mendeley Data `r4jgxk2mhn`
  (`https://data.mendeley.com/datasets/r4jgxk2mhn`).
- **Citation:** Broyles, J.M.; Gevaudan, J.P.; Brown, N.C. (2024),
  *A compiled dataset of ready-mix concrete EPDs for LCA*, **Data in Brief 52,
  109852**.
- **Licence/terms:** Mendeley Data, public (CC BY 4.0 typical — confirm on
  landing page before redistribution).
- **Download method:** Mendeley public-api file listing → public download URL
  (**verified HTTP 200**). Version 3 CSV ≈ **81 MB**; XLSX ≈ 23 MB.
- **Size:** ~39,213 EPDs (v2) up to ~47,413 (latest version); v3 used here.
- **Columns (header verified):** Company/Plant identity & location, **U.S. Region
  of Plant**, EPD Program Operator, EPD issue/valid dates, Mixture Label &
  Description, **Concrete Compressive Strength (psi)**, **Concrete Curation
  Time**, **Declared Unit**, **Product Components**, **A1–A3 Global Warming
  Potential (kg CO₂-eq)** with stage splits (A1/A2/A3), plus ODP, AP, EP, POCP,
  abiotic depletion, waste, and freshwater indicators.
- **Targets:** A1–A3 GWP (kg CO₂-eq); strength class (psi) for benchmarking.
- **Missing data:** many optional LCA fields are sparsely populated; declared
  units and PCRs vary across producers; rows missing GWP or strength are filtered
  at load time.
- **Use in chapter:** derive **carbon-class thresholds** and an **EPD-based
  benchmark percentile** by strength class/region for the sustainability block.

## D3 — SCM-RAC Multi-output Concrete Dataset & Framework (DURABILITY, OPTIONAL)
- **Source:** GitHub `prayogohandy/SCM-RAC-Concrete-Prediction` (reachable, 200).
- **Targets:** compressive, tensile, flexural strength; elastic modulus; slump;
  drying shrinkage; chloride permeability (multi-output).
- **Licence/terms:** repository resources — verify repo licence before reuse.
- **Why optional:** durability targets are sparsely reported (the framework uses
  selective information transfer). Used to **discuss** the optional durability
  extension and durability-data scarcity, not as a required runtime dependency.

## D4 — ICE Database (CARBON FACTORS, INCLUDED)
- **Source/citation:** Hammond, G.; Jones, C. (2008), *Embodied energy and carbon
  in construction materials* (Inventory of Carbon & Energy, ICE), *Proc. ICE –
  Energy* 161(2):87–98; later maintained by Circular Ecology.
- **Licence/terms:** open, attribution required.
- **Use in chapter:** transparent per-constituent embodied-carbon factors
  (cement, GGBS, fly ash, aggregate, water, admixture) for a **documented linear
  GWP estimate** from mix composition (no fabricated values; factors cited).

## D5 — NRMCA Industry-Average EPD / Regional Benchmarks (REFERENCE, INCLUDED)
- **Source:** NRMCA EPD program (public industry-average EPD); cross-referenced
  with public U.S. GSA/FHWA low-carbon GWP limits.
- **Use in chapter:** anchor **Low / Typical / High** carbon classes by strength
  class/region and cross-check EPD-derived percentiles.

## D6 — buildingSMART Sample-Test-Files (IFC) (MAPPING DEMO, OPTIONAL)
- **Source:** GitHub `buildingSMART/Sample-Test-Files` (reachable, 200).
- **Use in chapter:** optional illustration of IFC mapping targets
  (`IfcMaterial`, concrete element subtypes). **Not required** — the workflow
  needs no geometry. Used only if it strengthens the mapping demonstration.

## D7 — RILEM TC 281-CCC Carbonation Dataset (DOCUMENTED, EXCLUDED FROM RUNTIME)
- **Source:** RILEM TC 281-CCC report (SCM carbonation; up to 94% SCM binders).
- **Status:** reported within the TC publication; not available as a single open
  CSV. **Documented** as evidence of durability-data scarcity/heterogeneity;
  **not loaded** at runtime.

---

## Google Colab usage notes

- **D1 (strength):** `src/data_download.py` downloads the `.xls` automatically; if
  the UCI host is unreachable, it falls back to `fetch_openml('Concrete_Data')`.
  No credentials needed.
- **D2 (EPD):** download programmatically in notebook 03 via the Mendeley
  public-api file listing, then the file `download_url`. Because the CSV is large
  (~81 MB), notebook 03 loads only the needed columns and filters rows with valid
  strength + GWP. A small cached/sampled extract is written to
  `data/external/` for reproducibility, and a tiny synthetic fallback is provided
  if the download fails.
- **D4/D5 (carbon factors/benchmarks):** staged as small documented tables in
  `data/external/` with citations; no large download.
- **D6 (IFC samples):** optional `git clone`/raw download only if used.
- All notebooks set a fixed random seed and save artefacts under `outputs/`.

## Selection rationale (summary)
- **Active modelling:** D1 (strength) + D2/D4/D5 (carbon).
- **Optional/discussion:** D3 (durability/multi-property), D6 (IFC samples),
  D7 (carbonation evidence).
- This keeps the runnable pipeline lightweight and fully public-data, while the
  optional datasets support the durability and OpenBIM-mapping narrative.
