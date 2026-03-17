from pydantic import BaseModel

class RiskFactorResponse(BaseModel):
    patient_risk_factor_topic: str
    patient_risk_factor_description: str

class OrderDrugResponse(BaseModel):
    b_item_id: str
    item_common_name: str
    unit: str
    dose: float

class PrescriptionResponse(BaseModel):
    visit_id: str
    visit_hn: str
    visit_vn: str
    f_visit_type: str
    visit_begin_visit_time: str
    visit_diagnosis_notice: str
    visit_patient_type: str
    visit_queue: str
    visit_dx: str
    patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    visit_staff_doctor_discharge: str
    visit_deny_allergy: str
    visit_patient_age: str
    risk_factors: list[RiskFactorResponse]
    order_drugs: list[OrderDrugResponse]

class PrescriptionItemResponse(BaseModel):
    visit_id: str
    visit_hn: str
    visit_vn: str
    patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    visit_begin_visit_time: str
    status: str

class PrescriptionListResponse(BaseModel):
    prescriptions: list[PrescriptionItemResponse]

class DetectionItemResponse(BaseModel):
    t_order_drug_id: str
    detection_item_id: str
    item_common_name: str
    confidence: float
    quantity: int
    unit: str

class DetectionResponse(BaseModel):
    detection_id: str
    verified_by: str
    verified_at: str
    matched: list[DetectionItemResponse]
    missing: list[DetectionItemResponse]
    extra: list[DetectionItemResponse]

class DetectionListResponse(BaseModel):
    detections: list[DetectionResponse]