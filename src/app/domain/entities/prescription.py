from dataclasses import dataclass

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
class PastHistory:
    patient_past_history_topic: str

@dataclass
class FamilyHistory:
    patient_family_topic: str

@dataclass
class PatientHistory:
    past_history: list[PastHistory]
    family_history: list[FamilyHistory]

@dataclass
class DrugAllergy:
    drug_allergies: list[str]
    monitoring: list[str]
    suspected: list[str]

@dataclass
class Prescription:
    order_id: str
    visit_hn: str
    visit_vn: str
    status: str
    visit_begin_visit_time: str
    visit_diagnosis_notice: str
    visit_patient_type: str
    visit_dx: str
    f_patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    visit_staff_doctor_discharge: str
    visit_patient_age: str
    risk_factors: list[RiskFactor]
    history: PatientHistory
    drug_allergy: DrugAllergy
    payment: str
    symptom: str

@dataclass
class PrescriptionItem:
    order_id: str
    visit_hn: str
    visit_vn: str
    f_patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    visit_begin_visit_time: str
    status: str
    verified_by: str | None = None
@dataclass
class PrescriptionList:
    prescriptions: list[PrescriptionItem]
    total: int
    page: int
    size: int

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