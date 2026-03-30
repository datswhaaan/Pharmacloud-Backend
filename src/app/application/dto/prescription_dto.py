from dataclasses import dataclass

@dataclass 
class RiskFactorDTO:
    patient_risk_factor_topic: str
    patient_risk_factor_description: str

@dataclass
class OrderDrugDTO:
    b_item_id: str
    item_common_name: str
    b_item_drug_uom_id_purch: str
    order_drug_dose: str

@dataclass
class PrescriptionDTO:
    visit_id: str
    visit_hn: str
    visit_vn: str
    f_visit_type: str
    visit_begin_visit_time: str
    visit_diagnosis_notice: str
    visit_patient_type: str
    visit_queue: str
    visit_dx: str
    f_patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    visit_staff_doctor_discharge: str
    visit_deny_allergy: str
    visit_patient_age: str
    risk_factors: list[RiskFactorDTO]
    order_drugs: list[OrderDrugDTO]

@dataclass
class PrescriptionItemDTO:
    visit_id: str
    visit_hn: str
    visit_vn: str
    f_patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    visit_begin_visit_time: str
    status: str

@dataclass
class PrescriptionListDTO:
    prescriptions: list[PrescriptionItemDTO]
    total: int
    page: int
    size: int

@dataclass
class DetectionItemDTO:
    t_order_drug_id: str
    detection_item_id: str
    item_common_name: str
    confidence: str
    quantity: str
    unit: str

@dataclass
class DetectionDTO:
    detection_id: str
    verified_by: str
    verified_at: str
    matched: list[DetectionItemDTO]
    missing: list[DetectionItemDTO]
    extra: list[DetectionItemDTO]

@dataclass
class DetectionListDTO:
    detections: list[DetectionDTO]