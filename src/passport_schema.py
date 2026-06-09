"""
passport_schema.py  (scientific hardening)
==========================================
Concrete Performance Passport data model + JSON Schema + the scientific decision
logic (risk classification, QA/QC decision, evidence level, readiness scoring,
IDS readiness, decision-support level).

Blocks:
  1. bim_element      — element ID/type, required strength, material class, volume
  2. mix_and_test     — cement, water, SCMs, aggregates, admixture, age
  3. ml_outputs       — predicted strength, uncertainty, prediction interval,
                        risk class + decision rule, explanation
  4. sustainability   — GWP estimate, carbon class, EPD benchmark percentile,
                        benchmark group, durability indicator status
  5. qa_qc / decision — QA/QC decision, readiness score, IDS readiness,
                        decision-support level
  6. evidence         — data source type, reference, evidence level (A-D),
                        auditability note, DPP/CPR relevance note
  7. openbim_refs     — IFC entity, Pset, IDS requirement references

Every block records provenance so measured, predicted, EPD-benchmarked, derived,
and illustrative fields are never confused. No numeric precision is fabricated.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

# Element types used by the illustrative BIM context.
ELEMENT_TYPES = [
    "beam", "column", "slab", "wall", "footing", "pile", "bridge_deck", "pier",
]

# Element type -> IFC element subtype (IFC 4.3).
ELEMENT_IFC_TYPE = {
    "beam": "IfcBeam",
    "column": "IfcColumn",
    "slab": "IfcSlab",
    "wall": "IfcWall",
    "footing": "IfcFooting",
    "pile": "IfcPile",
    "bridge_deck": "IfcSlab (bridge deck)",
    "pier": "IfcColumn (bridge pier)",
}

QA_DECISIONS = ["Accept", "Review", "Hold", "Retest", "Missing Data"]
RISK_CLASSES = ["Low", "Medium", "High", "Unknown"]
EVIDENCE_LEVELS = ["A", "B", "C", "D"]
EVIDENCE_LEVEL_MEANING = {
    "A": "measured project/lab data",
    "B": "verified public dataset or EPD-derived benchmark",
    "C": "ML prediction from public data",
    "D": "illustrative, incomplete, or missing data",
}

# Fields that an IDS-ready passport must declare (drives readiness scoring).
REQUIRED_PASSPORT_FIELDS = [
    "material_class", "required_strength_mpa", "predicted_strength_mpa",
    "risk_class", "qa_qc_decision",
]
RECOMMENDED_PASSPORT_FIELDS = [
    "prediction_uncertainty_mpa", "carbon_class", "gwp_estimate_kgco2e_per_m3",
    "model_name", "volume_m3",
]

RISK_DECISION_RULE = (
    "Accept if predicted >= 1.05*required; Review if required <= predicted < "
    "1.05*required; Hold if 0.95*required <= predicted < required; Retest if "
    "predicted < 0.95*required or relative uncertainty > 0.20; Missing Data if "
    "required or predicted is unavailable."
)


def classify_qa(required: Optional[float], predicted: Optional[float],
                rel_uncertainty: Optional[float] = None) -> str:
    """QA/QC decision per documented thresholds (Accept/Review/Hold/Retest/Missing)."""
    if required is None or predicted is None or required <= 0:
        return "Missing Data"
    ru = rel_uncertainty if rel_uncertainty is not None else 0.0
    if predicted < 0.95 * required or ru > 0.20:
        return "Retest"
    if predicted < required:
        return "Hold"
    if predicted < 1.05 * required:
        return "Review"
    return "Accept"


def classify_risk(required: Optional[float], predicted: Optional[float],
                  rel_uncertainty: Optional[float]) -> str:
    """Risk class combining safety margin and relative prediction uncertainty."""
    if required is None or predicted is None or required <= 0:
        return "Unknown"
    margin = (predicted - required) / required
    ru = rel_uncertainty if rel_uncertainty is not None else 0.10
    if margin >= 0.05 and ru < 0.10:
        return "Low"
    if margin >= 0.0 and ru < 0.20:
        return "Medium"
    return "High"


def decision_support_level(predicted: Optional[float], carbon_class: str) -> str:
    """descriptive / predictive / prescriptive-lite."""
    if predicted is None:
        return "descriptive"
    if carbon_class and carbon_class not in ("Not assessed", "", None):
        return "prescriptive-lite"
    return "predictive"


def compute_readiness(flat: Dict) -> float:
    """0-100 completeness over required + recommended fields (required weighted 2x)."""
    req_present = sum(1 for f in REQUIRED_PASSPORT_FIELDS
                      if flat.get(f) not in (None, "", float("nan")))
    rec_present = sum(1 for f in RECOMMENDED_PASSPORT_FIELDS
                      if flat.get(f) not in (None, "", float("nan")))
    max_score = 2 * len(REQUIRED_PASSPORT_FIELDS) + len(RECOMMENDED_PASSPORT_FIELDS)
    score = (2 * req_present + rec_present) / max_score * 100.0
    return round(score, 1)


def ids_readiness(flat: Dict) -> str:
    """Pass / Partial / Fail against required IDS fields."""
    present = [f for f in REQUIRED_PASSPORT_FIELDS
               if flat.get(f) not in (None, "", float("nan"))]
    if len(present) == len(REQUIRED_PASSPORT_FIELDS):
        return "Pass"
    if len(present) == 0:
        return "Fail"
    return "Partial"


@dataclass
class BIMElement:
    element_id: str
    element_type: str
    required_strength_mpa: Optional[float]
    material_class: str
    volume_m3: Optional[float]
    ifc_element_type: str
    provenance: str = "illustrative_demonstration"


@dataclass
class MixAndTest:
    cement: float
    water: float
    blast_furnace_slag: float
    fly_ash: float
    silica_fume: Optional[float]
    coarse_aggregate: float
    fine_aggregate: float
    superplasticizer: float
    age_days: float
    water_binder_ratio: Optional[float]
    measured_strength_mpa: Optional[float]
    provenance: str = "dataset_derived (UCI, Yeh 1998)"


@dataclass
class MLOutputs:
    predicted_strength_mpa: float
    prediction_uncertainty_mpa: float
    relative_uncertainty: float
    model_confidence_or_uncertainty: str          # categorical Low/Medium/High
    prediction_interval_lower: Optional[float]
    prediction_interval_upper: Optional[float]
    uncertainty_method: str
    risk_class: str
    risk_decision_rule: str
    top_features: List[str]
    model_name: str
    provenance: str = "model_derived (ML prediction from public data)"


@dataclass
class Sustainability:
    gwp_estimate_kgco2e_per_m3: Optional[float]
    carbon_class: str                               # Low / Typical / High / Not assessed
    carbon_benchmark_group: str
    epd_benchmark_percentile: Optional[float]
    durability_indicator_status: str                # modeled/available/missing/future extension
    provenance: str = "ICE factors (estimate) + EPD benchmark (Broyles et al. 2024)"


@dataclass
class DecisionReadiness:
    qa_qc_decision: str
    passport_readiness_score: float
    ids_readiness_status: str
    decision_support_level: str
    rationale: str
    provenance: str = "rule_based"


@dataclass
class Evidence:
    data_source_type: str        # measured/predicted/EPD_benchmark/derived/illustrative/missing
    data_source_reference: str
    evidence_level: str          # A / B / C / D
    evidence_level_meaning: str
    auditability_note: str
    dpp_cpr_relevance_note: str = (
        "Aligned with the broader direction of digital product/performance "
        "information management (e.g., EU CPR Digital Product Passport); this is "
        "NOT a claim of legal/regulatory compliance.")


@dataclass
class OpenBIMRefs:
    ifc_material: str = "IfcMaterial / IfcMaterialConstituentSet"
    standard_pset: str = "Pset_MaterialConcrete; Pset_ConcreteElementGeneral"
    custom_pset: str = "Pset_ConcretePerformancePassport (proposed, NOT an official IFC Pset)"
    ids_requirement_ids: List[str] = field(default_factory=list)
    provenance: str = "specification_level (conceptual unless validated on real IFC)"


@dataclass
class Passport:
    bim_element: BIMElement
    mix_and_test: MixAndTest
    ml_outputs: MLOutputs
    sustainability: Sustainability
    decision: DecisionReadiness
    evidence: Evidence
    openbim_refs: OpenBIMRefs
    schema_version: str = "2.0"

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_flat_row(self) -> Dict:
        b, m, ml, s, d, e = (self.bim_element, self.mix_and_test, self.ml_outputs,
                             self.sustainability, self.decision, self.evidence)
        return {
            # BIM element
            "element_id": b.element_id,
            "element_type": b.element_type,
            "ifc_element_type": b.ifc_element_type,
            "material_class": b.material_class,
            "required_strength_mpa": b.required_strength_mpa,
            "volume_m3": b.volume_m3,
            # mix & test
            "cement": m.cement, "water": m.water,
            "blast_furnace_slag": m.blast_furnace_slag, "fly_ash": m.fly_ash,
            "coarse_aggregate": m.coarse_aggregate, "fine_aggregate": m.fine_aggregate,
            "superplasticizer": m.superplasticizer, "age_days": m.age_days,
            "water_binder_ratio": m.water_binder_ratio,
            "measured_strength_mpa": m.measured_strength_mpa,
            # ML outputs
            "predicted_strength_mpa": _r(ml.predicted_strength_mpa, 2),
            "prediction_uncertainty_mpa": _r(ml.prediction_uncertainty_mpa, 2),
            "relative_uncertainty": _r(ml.relative_uncertainty, 3),
            "model_confidence_or_uncertainty": ml.model_confidence_or_uncertainty,
            "prediction_interval_lower": _r(ml.prediction_interval_lower, 2),
            "prediction_interval_upper": _r(ml.prediction_interval_upper, 2),
            "uncertainty_method": ml.uncertainty_method,
            "risk_class": ml.risk_class,
            "risk_decision_rule": ml.risk_decision_rule,
            "top_features": ";".join(ml.top_features),
            "model_name": ml.model_name,
            # sustainability
            "gwp_estimate_kgco2e_per_m3": _r(s.gwp_estimate_kgco2e_per_m3, 1),
            "carbon_class": s.carbon_class,
            "carbon_benchmark_group": s.carbon_benchmark_group,
            "epd_benchmark_percentile": s.epd_benchmark_percentile,
            "durability_indicator_status": s.durability_indicator_status,
            # decision-readiness
            "qa_qc_decision": d.qa_qc_decision,
            "passport_readiness_score": d.passport_readiness_score,
            "ids_readiness_status": d.ids_readiness_status,
            "decision_support_level": d.decision_support_level,
            "qa_rationale": d.rationale,
            # evidence / provenance
            "data_source_type": e.data_source_type,
            "data_source_reference": e.data_source_reference,
            "evidence_level": e.evidence_level,
            "evidence_level_meaning": e.evidence_level_meaning,
            "auditability_note": e.auditability_note,
            "dpp_cpr_relevance_note": e.dpp_cpr_relevance_note,
        }


def _r(v, n):
    return None if v is None else round(float(v), n)


def json_schema() -> Dict:
    num = {"type": ["number", "null"]}
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "ConcretePerformancePassport",
        "type": "object",
        "required": ["bim_element", "mix_and_test", "ml_outputs",
                     "sustainability", "decision", "evidence", "openbim_refs"],
        "properties": {
            "bim_element": {"type": "object",
                "required": ["element_id", "element_type"],
                "properties": {
                    "element_id": {"type": "string"},
                    "element_type": {"type": "string", "enum": ELEMENT_TYPES},
                    "required_strength_mpa": num,
                    "material_class": {"type": "string"},
                    "volume_m3": num,
                    "ifc_element_type": {"type": "string"}}},
            "mix_and_test": {"type": "object",
                "properties": {k: num for k in [
                    "cement", "water", "blast_furnace_slag", "fly_ash", "silica_fume",
                    "coarse_aggregate", "fine_aggregate", "superplasticizer",
                    "age_days", "water_binder_ratio", "measured_strength_mpa"]}},
            "ml_outputs": {"type": "object",
                "required": ["predicted_strength_mpa", "risk_class"],
                "properties": {
                    "predicted_strength_mpa": {"type": "number"},
                    "prediction_uncertainty_mpa": num,
                    "relative_uncertainty": num,
                    "model_confidence_or_uncertainty": {"type": "string"},
                    "prediction_interval_lower": num,
                    "prediction_interval_upper": num,
                    "uncertainty_method": {"type": "string"},
                    "risk_class": {"type": "string", "enum": RISK_CLASSES},
                    "risk_decision_rule": {"type": "string"},
                    "top_features": {"type": "array", "items": {"type": "string"}},
                    "model_name": {"type": "string"}}},
            "sustainability": {"type": "object",
                "properties": {
                    "gwp_estimate_kgco2e_per_m3": num,
                    "carbon_class": {"type": "string",
                                     "enum": ["Low", "Typical", "High", "Not assessed"]},
                    "carbon_benchmark_group": {"type": "string"},
                    "epd_benchmark_percentile": num,
                    "durability_indicator_status": {"type": "string"}}},
            "decision": {"type": "object", "required": ["qa_qc_decision"],
                "properties": {
                    "qa_qc_decision": {"type": "string", "enum": QA_DECISIONS},
                    "passport_readiness_score": {"type": "number"},
                    "ids_readiness_status": {"type": "string",
                                             "enum": ["Pass", "Partial", "Fail"]},
                    "decision_support_level": {"type": "string"}}},
            "evidence": {"type": "object", "required": ["evidence_level"],
                "properties": {
                    "data_source_type": {"type": "string"},
                    "data_source_reference": {"type": "string"},
                    "evidence_level": {"type": "string", "enum": EVIDENCE_LEVELS},
                    "auditability_note": {"type": "string"},
                    "dpp_cpr_relevance_note": {"type": "string"}}},
            "openbim_refs": {"type": "object",
                "properties": {
                    "ifc_material": {"type": "string"},
                    "standard_pset": {"type": "string"},
                    "custom_pset": {"type": "string"},
                    "ids_requirement_ids": {"type": "array", "items": {"type": "string"}}}},
        },
    }
