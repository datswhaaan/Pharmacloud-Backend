from dataclasses import dataclass
from datetime import datetime

@dataclass
class RiskFactor:
    patient_risk_factor_topic: str
    patient_risk_factor_description: str

@dataclass
class OrderDrug:
    b_item_id: str
    item_common_name: str
    b_item_drug_uom_id_purch: str
    order_drug_dose: str

@dataclass
class Prescription:
    t_visit_id: str
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
    risk_factors: list[RiskFactor]
    order_drugs: list[OrderDrug]

@dataclass
class PrescriptionItem:
    t_visit_id: str
    visit_hn: str
    visit_vn: str
    f_patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    visit_begin_visit_time: str
    status: str

@dataclass
class PrescriptionList:
    prescriptions: list[PrescriptionItem]

@dataclass
class DetectionItem:
    detection_item_id: str
    b_item_id: str
    item_common_name: str
    confidence: str

@dataclass
class Detection:
    detection_id: str
    detected_at: datetime
    image_url: str
    verified_by: str
    verified_at: datetime
    detections: list[DetectionItem]

@dataclass
class DetectionList:
    detections: list[Detection]

@dataclass
class OrderDrugItem:
    t_order_drug_id: str
    b_item_id: str
    item_common_name: str
    unit: str
    quantity: str

@dataclass
class OrderList:
    orders: list[OrderDrugItem]