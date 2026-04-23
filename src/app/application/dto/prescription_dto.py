from dataclasses import dataclass

@dataclass 
class RiskFactorDTO:
    alcoholUse: str
    smokingHabits: str

@dataclass
class OrderDrugDTO:
    t_order_drug_id: str
    item_common_name: str
    unit: str
    quantity: str

@dataclass
class OrderDrugInferDTO:
    t_order_drug_id: str
    item_common_name: str
    unit: str
    quantity: str
    match_type: str

@dataclass
class PastHistoryDTO:
    patient_past_history_topic: str

@dataclass
class FamilyHistoryDTO:
    patient_family_history_topic: str

@dataclass
class PatientHistoryDTO:
    past_history: list[PastHistoryDTO]
    family_history: list[FamilyHistoryDTO]

@dataclass
class DrugAllergyDTO:
    drug_allergies: list[str]
    monitoring: list[str]
    suspected: list[str]

@dataclass
class PrescriptionDTO:
    order_id: str
    visit_hn: str
    visit_vn: str
    status: str
    visit_begin_visit_time: str
    visit_diagnosis_notice: str
    visit_patient_type: str
    visit_dx: str
    patient_name: str
    visit_staff_doctor_discharge: str
    visit_patient_age: str
    risk_factors: RiskFactorDTO
    history: PatientHistoryDTO
    drug_allergy: DrugAllergyDTO
    payment: str
    symptom: str

@dataclass
class PrescriptionItemDTO:
    order_id: str
    visit_hn: str
    visit_vn: str
    f_patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    visit_begin_visit_time: str
    status: str
    verified_by: str

@dataclass
class PrescriptionListDTO:
    prescriptions: list[PrescriptionItemDTO]
    total: int
    page: int
    size: int