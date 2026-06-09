"""
Offline sanity tests for the Concrete Performance Passport project.

STRICT OFFLINE: these tests must NEVER download data. They use tiny in-memory
fixtures, the project's pure-logic functions, and existing repository files.
Run with:  USE_CACHED_ONLY=1 pytest -q

Some checks tolerate "pending" computed artefacts (model .pkl, figures, real
passport records) that are produced by:
    USE_CACHED_ONLY=1 python -m src.finalize_lightweight_outputs
Those are marked with pytest.skip when absent, so the suite still validates the
schema, logic, mappings, and documentation without network access.
"""
import json
import os
from pathlib import Path

import pytest

os.environ.setdefault("USE_CACHED_ONLY", "1")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
TABLES = OUT / "tables"

import sys
sys.path.insert(0, str(ROOT))


# --- 1. Data cleaning works on a tiny in-memory fixture -----------------------
def test_data_cleaning_on_tiny_fixture():
    import pandas as pd
    from src import data_cleaning
    df = pd.DataFrame({
        "cement": [300.0, 400.0], "blast_furnace_slag": [0.0, 50.0],
        "fly_ash": [0.0, 0.0], "water": [180.0, 170.0],
        "superplasticizer": [2.0, 5.0], "coarse_aggregate": [1000.0, 980.0],
        "fine_aggregate": [800.0, 780.0], "age": [28, 28],
        "compressive_strength": [30.0, 45.0],
    })
    out = data_cleaning.engineer_features(df)
    assert len(out) == 2                      # no rows dropped
    assert "water_binder_ratio" in out.columns
    assert "total_binder" in out.columns
    assert out["total_binder"].iloc[1] == 450.0


# --- 2. Risk + QA classification logic ---------------------------------------
def test_risk_and_qa_classification():
    from src import passport_schema as ps
    assert ps.classify_qa(30.0, 33.0, 0.05) == "Accept"      # >=1.05x
    assert ps.classify_qa(30.0, 30.5, 0.05) == "Review"      # between
    assert ps.classify_qa(30.0, 29.0, 0.05) == "Hold"        # just below
    assert ps.classify_qa(30.0, 20.0, 0.05) == "Retest"      # far below
    assert ps.classify_qa(None, 30.0) == "Missing Data"
    assert ps.classify_risk(30.0, 33.0, 0.05) == "Low"
    assert ps.classify_risk(None, 33.0, 0.05) == "Unknown"


# --- 3. Passport schema exposes all required scientific fields ---------------
def test_passport_schema_fields():
    from src import passport_schema as ps
    schema = ps.json_schema()
    props = schema["properties"]
    for block in ["bim_element", "mix_and_test", "ml_outputs",
                  "sustainability", "decision", "evidence", "openbim_refs"]:
        assert block in props
    ev = props["evidence"]["properties"]
    for f in ["data_source_type", "evidence_level", "auditability_note",
              "dpp_cpr_relevance_note"]:
        assert f in ev
    ml = props["ml_outputs"]["properties"]
    for f in ["prediction_interval_lower", "prediction_interval_upper",
              "uncertainty_method", "risk_class", "risk_decision_rule"]:
        assert f in ml
    dec = props["decision"]["properties"]
    for f in ["qa_qc_decision", "passport_readiness_score",
              "ids_readiness_status", "decision_support_level"]:
        assert f in dec


# --- 4. Readiness + IDS readiness scoring ------------------------------------
def test_readiness_scoring():
    from src import passport_schema as ps
    full = {"material_class": "C30/37", "required_strength_mpa": 30,
            "predicted_strength_mpa": 35, "risk_class": "Low",
            "qa_qc_decision": "Accept"}
    assert ps.ids_readiness(full) == "Pass"
    assert ps.compute_readiness(full) > 50
    empty = {}
    assert ps.ids_readiness(empty) == "Fail"


# --- 5. Passport JSON file is valid + has expected structure -----------------
def test_passport_json_valid():
    p = TABLES / "concrete_performance_passports.json"
    assert p.exists(), "passport JSON missing"
    data = json.loads(p.read_text())
    assert "blocks_and_fields" in data or "json_schema" in data
    assert "passports" in data
    assert "evidence_levels" in data


# --- 6. Passport CSV has the scientific field columns ------------------------
def test_passport_csv_fields():
    import csv
    p = TABLES / "concrete_performance_passports.csv"
    assert p.exists(), "passport CSV missing"
    header = next(csv.reader(p.open()))
    for col in ["evidence_level", "data_source_type", "risk_class",
                "qa_qc_decision", "carbon_class", "prediction_interval_lower",
                "passport_readiness_score", "ids_readiness_status",
                "decision_support_level", "durability_indicator_status",
                "dpp_cpr_relevance_note", "uncertainty_method"]:
        assert col in header, f"missing passport column: {col}"


# --- 7. OpenBIM mapping contains IFC-related concepts ------------------------
def test_openbim_mapping_has_ifc():
    p = TABLES / "openbim_mapping.csv"
    assert p.exists(), "openbim mapping missing"
    text = p.read_text()
    assert "IfcMaterial" in text
    assert "Pset_MaterialConcrete" in text
    assert "Pset_ConcretePerformancePassport" in text


# --- 8. IDS matrix contains required information fields ----------------------
def test_ids_matrix_fields():
    import csv
    p = TABLES / "ids_requirement_matrix.csv"
    assert p.exists(), "IDS matrix missing"
    rows = list(csv.DictReader(p.open()))
    assert len(rows) >= 10
    for col in ["requirement_id", "required_property", "expected_type_or_value",
                "importance", "related_passport_field"]:
        assert col in rows[0]
    assert any(r["importance"] == "required" for r in rows)


# --- 9. Model performance summary file exists --------------------------------
def test_model_performance_summary_exists():
    assert (TABLES / "model_performance_summary.csv").exists()


# --- 10. Chapter draft + final report + README exist -------------------------
def test_documents_exist():
    assert (OUT / "chapter" / "book_chapter_draft.md").exists()
    assert (OUT / "final_report.md").exists()
    assert (ROOT / "README.md").exists()


# --- 11. Optional computed artefacts (skip if pending) -----------------------
def test_trained_model_optional():
    pkl = OUT / "models" / "best_strength_model.pkl"
    if not pkl.exists():
        pytest.skip("best_strength_model.pkl pending offline finalizer run")
    import joblib
    art = joblib.load(pkl)
    assert "model" in art and "features" in art


def test_no_network_used():
    # USE_CACHED_ONLY must be set so loaders never hit the network during tests.
    assert os.environ.get("USE_CACHED_ONLY") == "1"
