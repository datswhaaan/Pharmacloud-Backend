from pydantic import BaseModel

class RiskFactorResponse(BaseModel):
    alcoholUse: str
    smokingHabits: str

class OrderDrugResponse(BaseModel):
    t_order_drug_id: str
    item_common_name: str
    unit: str
    quantity: float

class PatientHistoryResponse(BaseModel):
    past_history: list[str]
    family_history: list[str]

class DrugAllergyResponse(BaseModel):
    drug_allergies: list[str]
    monitoring: list[str]
    suspected: list[str]

class PrescriptionResponse(BaseModel):
    order_id: str
    visit_hn: str
    visit_vn: str
    symptom: str
    status: str
    payment: str
    visit_begin_visit_time: str
    visit_diagnosis_notice: str
    visit_patient_type: str
    visit_dx: str
    patient_name: str
    visit_staff_doctor_discharge: str
    visit_patient_age: str
    risk_factors: RiskFactorResponse
    history: PatientHistoryResponse
    drug_allergy: DrugAllergyResponse

class PrescriptionItemResponse(BaseModel):
    order_id: str
    visit_hn: str
    visit_vn: str
    patient_name: str
    visit_begin_visit_time: str
    status: str

class PrescriptionListResponse(BaseModel):
    prescriptions: list[PrescriptionItemResponse]
    total: int
    page: int
    size: int

class DetectionItemResponse(BaseModel):
    t_order_drug_id: str
    detection_item_id: str
    item_common_name: str
    confidence: float
    confidence_level: str
    quantity: int
    unit: str
    is_manually_edited: bool
    match_type: str

class DetectionResponse(BaseModel):
    detection_id: str
    image_url: str
    status: str
    verified_by: str
    verified_at: str
    drug_list: list[DetectionItemResponse]

class DetectionListResponse(BaseModel):
    order_drugs: list[OrderDrugResponse]
    detections: list[DetectionResponse]