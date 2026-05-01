from app.domain.entities.prescription import Prescription, PrescriptionList, RiskFactor, OrderDrug
from app.application.dto.prescription_dto import PrescriptionDTO, PrescriptionItemDTO, PrescriptionListDTO, RiskFactorDTO, PatientHistoryDTO, PastHistoryDTO, FamilyHistoryDTO, DrugAllergyDTO, OrderDrugInferDTO

def _risk_factors_mapper(riskFactors: list[RiskFactor]) -> RiskFactorDTO:
    alcohol = ""
    smoking = ""

    for riskFactor in riskFactors:
        if riskFactor.patient_risk_factor_topic == "การดื่มแอลกอฮอล์":
            alcohol = riskFactor.patient_risk_factor_description
        elif riskFactor.patient_risk_factor_topic == "การสูบบุหรี่":
            smoking = riskFactor.patient_risk_factor_description

    return RiskFactorDTO(
        alcoholUse=alcohol,
        smokingHabits=smoking
    )

def _to_prescription_dto(prescription: Prescription) -> PrescriptionDTO:
    return PrescriptionDTO(
        order_id=prescription.order_id,
        visit_hn=prescription.visit_hn,
        visit_vn=prescription.visit_vn,
        status=_status_mapper(prescription.status),
        visit_begin_visit_time=prescription.visit_begin_visit_time,
        visit_diagnosis_notice=prescription.visit_diagnosis_notice,
        visit_patient_type=prescription.visit_patient_type,
        visit_dx=prescription.visit_dx,
        patient_name=prescription.f_patient_prefix + prescription.patient_firstname + " " + prescription.patient_lastname,
        visit_staff_doctor_discharge=prescription.visit_staff_doctor_discharge,
        visit_patient_age=prescription.visit_patient_age,
        risk_factors=_risk_factors_mapper(prescription.risk_factors),
        history=PatientHistoryDTO(
            past_history=[
                PastHistoryDTO(
                    patient_past_history_topic=ph.patient_past_history_topic
                ) for ph in prescription.history.past_history
            ],
            family_history=[
                FamilyHistoryDTO(
                    patient_family_history_topic=fh.patient_family_topic
                ) for fh in prescription.history.family_history
            ]
        ),
        drug_allergy=DrugAllergyDTO(
            drug_allergies=prescription.drug_allergy.drug_allergies,
            monitoring=prescription.drug_allergy.monitoring,
            suspected=prescription.drug_allergy.suspected
        ),
        payment=prescription.payment,
        symptom=prescription.symptom
    )

def _to_prescription_list_dto(prescription_list: PrescriptionList) -> PrescriptionListDTO:
    return PrescriptionListDTO(
        prescriptions=[
            PrescriptionItemDTO(
                order_id=prescription.order_id,
                visit_hn=prescription.visit_hn,
                visit_vn=prescription.visit_vn,
                f_patient_prefix=prescription.f_patient_prefix,
                patient_firstname=prescription.patient_firstname,
                patient_lastname=prescription.patient_lastname,
                visit_begin_visit_time=prescription.visit_begin_visit_time,
                status=_status_mapper(prescription.status),
                verified_by=prescription.verified_by
            )
            for prescription in prescription_list.prescriptions
        ],
        total=prescription_list.total,
        page=prescription_list.page,
        size=prescription_list.size
    )

def _to_order_drug_infer_dto(ordered: OrderDrug, match_type: str) -> OrderDrugInferDTO:
    return OrderDrugInferDTO(
        t_order_drug_id=ordered.t_order_drug_id,
        item_common_name=ordered.item_common_name,
        unit=ordered.unit,
        quantity=ordered.quantity,
        match_type=match_type
    )

def _status_mapper(status_id: str) -> str:
    mapping = {
        '1': "COMPLETED",
        '2': "WAITING",
        '6': "COMPLETED",
        '4': "WAITING",
        '3': "COMPLETED",
        '5': "CANCELLED"
    }
    return mapping.get(status_id, "UNKNOWN")