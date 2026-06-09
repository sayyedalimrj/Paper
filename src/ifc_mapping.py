"""
ifc_mapping.py  (Phase 5 — implemented)
=======================================
Maps Concrete Performance Passport fields to OpenBIM/IFC concepts and emits
IDS-ready artefacts. ifcopenshell is OPTIONAL: if unavailable, a conceptual
mapping + IDS requirement matrix + a hand-written IDS-style XML are still
produced (no blocking).

Outputs:
  * outputs/tables/openbim_mapping.csv
  * outputs/tables/ids_requirement_matrix.csv
  * outputs/tables/Pset_ConcretePerformancePassport.csv  (proposed Pset)
  * outputs/chapter/concrete_performance_passport.ids.xml  (conceptual IDS)
  * outputs/tables/ifc_extraction_demo.csv  (only if ifcopenshell + sample IFC)
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

try:
    from src import config, utils
except ImportError:
    import config, utils  # type: ignore

LOG = utils.get_logger("ifc_mapping")


# -----------------------------------------------------------------------------
# 1. Passport field -> IFC mapping
# -----------------------------------------------------------------------------
def openbim_mapping() -> pd.DataFrame:
    rows = [
        # passport_field, description, suggested_ifc_entity_or_pset, example_ifc_concept, required, data_type, use
        ("element_id", "Unique element identifier", "IfcRoot.GlobalId / Tag",
         "IfcColumn.GlobalId", "Required", "IfcGloballyUniqueId/string", "QA/QC"),
        ("element_type", "Structural element type", "IfcElement subtype",
         "IfcBeam, IfcColumn, IfcSlab, IfcWall, IfcFooting, IfcPile", "Required", "enum", "QA/QC"),
        ("material_class", "Concrete class / grade", "IfcMaterial.Name + IfcClassificationReference",
         "IfcMaterial(Name='C30/37')", "Required", "IfcLabel/string", "QA/QC"),
        ("required_strength_mpa", "Specified characteristic strength", "Pset_ConcreteElementGeneral / Pset_MaterialConcrete",
         "Pset_MaterialConcrete.CompressiveStrength", "Required", "IfcPressureMeasure (Pa)", "QA/QC"),
        ("measured_strength_mpa", "Lab/test compressive strength", "Pset_MaterialConcrete (property history)",
         "Pset_MaterialConcrete.CompressiveStrength", "Optional", "IfcPressureMeasure (Pa)", "QA/QC"),
        ("cement|water|scm|aggregate|admixture", "Mix-design constituents (kg/m3)",
         "IfcMaterialConstituentSet / IfcMaterialConstituent", "IfcMaterialConstituent(Name='Cement')",
         "Optional", "IfcMassMeasure per volume", "QA/QC + sustainability"),
        ("water_binder_ratio", "Water/binder ratio", "Custom Pset",
         "Pset_ConcretePerformancePassport.WaterBinderRatio", "Optional", "IfcRatioMeasure", "QA/QC"),
        ("age_days", "Age at test/assessment", "Custom Pset / Pset_ConcreteElementGeneral",
         "Pset_ConcretePerformancePassport.AgeAtAssessment", "Optional", "IfcTimeMeasure (days)", "QA/QC"),
        ("predicted_strength_mpa", "ML-predicted compressive strength", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.PredictedCompressiveStrength", "Required", "IfcPressureMeasure (Pa)", "QA/QC"),
        ("prediction_uncertainty_mpa", "Prediction uncertainty (1 sigma)", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.PredictionUncertainty", "Optional", "IfcPressureMeasure (Pa)", "QA/QC"),
        ("risk_class", "Risk class (Low/Medium/High)", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.RiskClass", "Required", "IfcLabel/enum", "QA/QC"),
        ("top_features", "Explanation: top contributing features", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.PredictionExplanation", "Optional", "IfcText", "QA/QC"),
        ("model_name", "Predictive model identifier", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.ModelReference", "Optional", "IfcLabel", "QA/QC"),
        ("gwp_estimate_kgco2e_per_m3", "Embodied carbon (A1-A3 GWP)", "IfcMaterial + EnvironmentalImpactValues / Custom Pset",
         "Pset_ConcretePerformancePassport.GWP_A1A3", "Optional", "IfcMassMeasure (kgCO2e/m3)", "Sustainability"),
        ("carbon_class", "Carbon class (Low/Typical/High)", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.CarbonClass", "Optional", "IfcLabel/enum", "Sustainability"),
        ("epd_benchmark_percentile", "EPD benchmark percentile", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.EPDBenchmarkPercentile", "Optional", "IfcRatioMeasure (%)", "Sustainability"),
        ("qa_decision", "QA/QC decision", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.QADecision", "Required", "IfcLabel/enum", "QA/QC"),
        ("evidence_level", "Evidence level (A-D) of the record", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.EvidenceLevel", "Required", "IfcLabel/enum", "QA/QC + provenance"),
        ("data_source_type", "Provenance of the decision value", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.DataSourceType", "Optional", "IfcLabel/enum", "QA/QC + provenance"),
        ("prediction_interval", "Approx. 95% prediction interval (bounds)", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.PredictionInterval", "Optional", "IfcPressureMeasure (Pa) bounds", "QA/QC"),
        ("passport_readiness_score", "Completeness score (0-100)", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.ReadinessScore", "Optional", "IfcRatioMeasure", "QA/QC"),
        ("durability_indicator_status", "Durability layer status", "Custom Pset (proposed)",
         "Pset_ConcretePerformancePassport.DurabilityStatus", "Optional", "IfcLabel/enum", "Durability"),
        ("volume_m3", "Element concrete volume", "IfcElementQuantity",
         "Qto_ConcreteElementBaseQuantities.NetVolume", "Optional", "IfcVolumeMeasure (m3)", "Sustainability"),
    ]
    cols = ["passport_field", "description", "suggested_ifc_entity_or_pset",
            "example_ifc_concept", "required_status", "data_type", "use_in_qaqc_or_sustainability"]
    df = pd.DataFrame(rows, columns=cols)
    path = config.TABLES_DIR / "openbim_mapping.csv"
    df.to_csv(path, index=False)
    LOG.info("Saved OpenBIM mapping -> %s", path)
    return df


# -----------------------------------------------------------------------------
# 2. Proposed custom property set
# -----------------------------------------------------------------------------
def proposed_pset() -> pd.DataFrame:
    rows = [
        ("PredictedCompressiveStrength", "IfcPressureMeasure", "ML-predicted 28-day (or age) compressive strength"),
        ("PredictionUncertainty", "IfcPressureMeasure", "Prediction uncertainty (1 standard deviation)"),
        ("RiskClass", "IfcLabel", "Low / Medium / High"),
        ("QADecision", "IfcLabel", "Accept / Review / Hold-Retest / Missing-Insufficient"),
        ("PredictionExplanation", "IfcText", "Top contributing features (e.g., SHAP)"),
        ("ModelReference", "IfcLabel", "Model name/version + dataset reference"),
        ("WaterBinderRatio", "IfcRatioMeasure", "Water-to-binder ratio"),
        ("AgeAtAssessment", "IfcTimeMeasure", "Concrete age at prediction/test (days)"),
        ("GWP_A1A3", "IfcMassMeasure", "Cradle-to-gate embodied carbon (kg CO2e per m3)"),
        ("CarbonClass", "IfcLabel", "Low / Typical / High"),
        ("EPDBenchmarkPercentile", "IfcRatioMeasure", "Percentile vs EPD benchmark within strength class"),
        ("EvidenceLevel", "IfcLabel", "Evidence level A/B/C/D of the decision value"),
        ("DataSourceType", "IfcLabel", "measured / predicted / EPD_benchmark / derived / illustrative / missing"),
        ("ReadinessScore", "IfcRatioMeasure", "Passport completeness score (0-100)"),
        ("PredictionIntervalLower", "IfcPressureMeasure", "Approx. 95% prediction-interval lower bound"),
        ("PredictionIntervalUpper", "IfcPressureMeasure", "Approx. 95% prediction-interval upper bound"),
        ("DurabilityStatus", "IfcLabel", "modeled / available / missing / future extension"),
        ("DecisionSupportLevel", "IfcLabel", "descriptive / predictive / prescriptive-lite"),
        ("PassportSchemaVersion", "IfcLabel", "Concrete Performance Passport schema version"),
    ]
    df = pd.DataFrame(rows, columns=["property_name", "ifc_value_type", "definition"])
    df.insert(0, "pset_name", "Pset_ConcretePerformancePassport")
    df["applicable_entities"] = "IfcBeam, IfcColumn, IfcSlab, IfcWall, IfcFooting, IfcPile (concrete)"
    path = config.TABLES_DIR / "Pset_ConcretePerformancePassport.csv"
    df.to_csv(path, index=False)
    LOG.info("Saved proposed Pset -> %s", path)
    return df


# -----------------------------------------------------------------------------
# 3. IDS-ready requirement matrix
# -----------------------------------------------------------------------------
def ids_requirement_matrix() -> pd.DataFrame:
    rows = [
        ("IDS-CPP-01", "Concrete material assigned", "IfcBeam/IfcColumn/IfcSlab/IfcWall/IfcFooting/IfcPile",
         "IfcMaterial.Name", "non-empty string (concrete class, e.g. C30/37)", "required",
         "Every concrete element must declare its material/class", "material_class"),
        ("IDS-CPP-02", "Specified compressive strength present", "concrete IfcElement",
         "Pset_MaterialConcrete.CompressiveStrength", ">0 Pa", "required",
         "Required strength must be available to evaluate QA", "required_strength_mpa"),
        ("IDS-CPP-03", "Mix constituents declared", "IfcMaterialConstituentSet",
         "IfcMaterialConstituent (Cement, Water, SCM, Aggregate)", "constituents present", "optional",
         "Supports sustainability + traceability", "cement|water|scm|aggregate"),
        ("IDS-CPP-04", "Predicted strength present", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.PredictedCompressiveStrength", ">0 Pa", "required",
         "Core ML output of the passport", "predicted_strength_mpa"),
        ("IDS-CPP-05", "Risk class declared", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.RiskClass", "enum {Low,Medium,High}", "required",
         "Drives prioritisation/decision", "risk_class"),
        ("IDS-CPP-06", "QA/QC decision declared", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.QADecision",
         "enum {Accept,Review,Hold/Retest,Missing/Insufficient}", "required",
         "The actionable QA outcome", "qa_decision"),
        ("IDS-CPP-07", "Prediction uncertainty present", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.PredictionUncertainty", ">=0 Pa", "optional",
         "Quantifies confidence", "prediction_uncertainty_mpa"),
        ("IDS-CPP-08", "Carbon class declared", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.CarbonClass", "enum {Low,Typical,High}", "optional",
         "Sustainability decision support", "carbon_class"),
        ("IDS-CPP-09", "Embodied carbon value present", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.GWP_A1A3", ">0 kgCO2e/m3", "optional",
         "Enables benchmarking", "gwp_estimate_kgco2e_per_m3"),
        ("IDS-CPP-10", "Model reference present", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.ModelReference", "non-empty string", "optional",
         "Traceability/auditability of the prediction", "model_name"),
        ("IDS-CPP-11", "Evidence level declared", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.EvidenceLevel", "enum {A,B,C,D}", "required",
         "Records the evidence basis (measured/public/ML/illustrative) for auditability", "evidence_level"),
        ("IDS-CPP-12", "Prediction interval / uncertainty present", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.PredictionInterval", "two bounds in Pa (approx)", "optional",
         "Communicates confidence around the prediction", "prediction_interval_lower/upper"),
        ("IDS-CPP-13", "Passport readiness score present", "concrete IfcElement",
         "Pset_ConcretePerformancePassport.ReadinessScore", "0-100", "optional",
         "Quantifies completeness/decision-readiness of the record", "passport_readiness_score"),
    ]
    cols = ["requirement_id", "requirement_name", "target_object_or_material",
            "required_property", "expected_type_or_value", "importance",
            "rationale", "related_passport_field"]
    df = pd.DataFrame(rows, columns=cols)
    path = config.TABLES_DIR / "ids_requirement_matrix.csv"
    df.to_csv(path, index=False)
    LOG.info("Saved IDS requirement matrix -> %s", path)
    return df


# -----------------------------------------------------------------------------
# 4. Conceptual IDS XML (hand-written, schema-style; not a certified IDS file)
# -----------------------------------------------------------------------------
def write_ids_xml(matrix: pd.DataFrame) -> Path:
    config.CHAPTER_DIR.mkdir(parents=True, exist_ok=True)
    specs = []
    for _, r in matrix.iterrows():
        specs.append(f"""    <specification name="{_xml(r['requirement_name'])}" ifcVersion="IFC4X3"
                   identifier="{r['requirement_id']}" minOccurs="{'1' if r['importance']=='required' else '0'}">
      <applicability>
        <entity><name><simpleValue>{_entity_for(r['target_object_or_material'])}</simpleValue></name></entity>
      </applicability>
      <requirements>
        <property dataType="IFCLABEL">
          <propertySet><simpleValue>{_pset_for(r['required_property'])}</simpleValue></propertySet>
          <baseName><simpleValue>{_prop_for(r['required_property'])}</simpleValue></baseName>
          <!-- expected: {_xml(str(r['expected_type_or_value']))} ; rationale: {_xml(str(r['rationale']))} -->
        </property>
      </requirements>
    </specification>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- CONCEPTUAL IDS (buildingSMART Information Delivery Specification style).
     Illustrative, not a certified/validated IDS file. Demonstrates how Concrete
     Performance Passport requirements can be expressed for automatic checking. -->
<ids xmlns="http://standards.buildingsmart.org/IDS"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <info>
    <title>Concrete Performance Passport - Information Delivery Specification</title>
    <description>Machine-checkable information requirements for concrete element performance passports.</description>
    <author>generated@concrete-performance-passport</author>
    <version>1.0</version>
  </info>
  <specifications>
{chr(10).join(specs)}
  </specifications>
</ids>
"""
    path = config.CHAPTER_DIR / "concrete_performance_passport.ids.xml"
    path.write_text(xml, encoding="utf-8")
    LOG.info("Saved conceptual IDS XML -> %s", path)
    return path


def _xml(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _entity_for(target: str) -> str:
    return "IFCBEAM"  # applicability simplified; real IDS would enumerate concrete subtypes


def _pset_for(prop: str) -> str:
    return prop.split(".")[0] if "." in prop else "Pset_ConcretePerformancePassport"


def _prop_for(prop: str) -> str:
    return prop.split(".")[1] if "." in prop else prop


# -----------------------------------------------------------------------------
# 5. Optional IfcOpenShell extraction demo
# -----------------------------------------------------------------------------
def optional_ifc_demo() -> str:
    try:
        import ifcopenshell  # noqa: F401
    except Exception as e:  # noqa: BLE001
        msg = (f"ifcopenshell not available ({type(e).__name__}); skipping IFC extraction demo. "
               "Conceptual mapping + IDS artefacts were produced instead (no blocking).")
        LOG.info(msg)
        return msg
    # If available, we would load a public sample IFC and extract IfcMaterial.
    try:
        import ifcopenshell
        # Create a tiny in-memory IFC to demonstrate material extraction without external files.
        f = ifcopenshell.file(schema="IFC4")
        mat = f.create_entity("IfcMaterial", Name="C30/37")
        df = pd.DataFrame([{"ifc_entity": "IfcMaterial", "name": mat.Name,
                            "note": "in-memory demo material created via ifcopenshell"}])
        df.to_csv(config.TABLES_DIR / "ifc_extraction_demo.csv", index=False)
        return "ifcopenshell available; wrote outputs/tables/ifc_extraction_demo.csv"
    except Exception as e:  # noqa: BLE001
        return f"ifcopenshell present but demo failed ({e}); conceptual artefacts used."


def build_mapping() -> Dict:
    config.ensure_dirs()
    mp = openbim_mapping()
    pset = proposed_pset()
    matrix = ids_requirement_matrix()
    ids_path = write_ids_xml(matrix)
    ifc_note = optional_ifc_demo()
    return {"mapping": mp, "pset": pset, "ids_matrix": matrix,
            "ids_xml": ids_path, "ifc_note": ifc_note}


if __name__ == "__main__":
    r = build_mapping()
    print("OpenBIM mapping rows:", len(r["mapping"]))
    print("IDS requirements:", len(r["ids_matrix"]))
    print("IFC demo:", r["ifc_note"])
