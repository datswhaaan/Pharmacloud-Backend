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

class PrescriptionListResponse(BaseModel):
    prescriptions: list[PrescriptionItemResponse]