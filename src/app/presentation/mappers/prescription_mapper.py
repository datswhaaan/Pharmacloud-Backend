
from app.application.dto.prescription_dto import PrescriptionDTO, PrescriptionListDTO
from app.presentation.schemas.prescription_response import PrescriptionItemResponse, PrescriptionListResponse, PrescriptionListResponse, PrescriptionResponse, RiskFactorResponse, OrderDrugResponse

def _to_prescription_response(dto: PrescriptionDTO) -> PrescriptionResponse:

    risk_factors = [
        RiskFactorResponse(
            patient_risk_factor_topic=rf.patient_risk_factor_topic,
            patient_risk_factor_description=rf.patient_risk_factor_description
        )
        for rf in dto.risk_factors
    ]

    order_drugs = [
        OrderDrugResponse(
            b_item_id=od.b_item_id,
            item_common_name=od.item_common_name,
            unit=od.b_item_drug_uom_id_purch,
            dose=od.order_drug_dose
        )
        for od in dto.order_drugs
    ]

    return PrescriptionResponse(
        visit_id=dto.visit_id,
        visit_hn=dto.visit_hn,
        visit_vn=dto.visit_vn,
        f_visit_type=dto.f_visit_type,
        visit_begin_visit_time=dto.visit_begin_visit_time,
        visit_diagnosis_notice=dto.visit_diagnosis_notice,
        visit_patient_type=dto.visit_patient_type,
        visit_queue=dto.visit_queue,
        visit_dx=dto.visit_dx,
        patient_prefix=dto.f_patient_prefix,
        patient_firstname=dto.patient_firstname,
        patient_lastname=dto.patient_lastname,
        visit_staff_doctor_discharge=dto.visit_staff_doctor_discharge,
        visit_deny_allergy=dto.visit_deny_allergy,
        visit_patient_age=dto.visit_patient_age,
        risk_factors=risk_factors,
        order_drugs=order_drugs
    )

def _to_prescription_list_response(dto: PrescriptionListDTO) -> PrescriptionListResponse:
    return PrescriptionListResponse(
        prescriptions=[
            PrescriptionItemResponse(
                visit_id=item.visit_id,
                visit_hn=item.visit_hn,
                visit_vn=item.visit_vn,
                patient_prefix=item.f_patient_prefix,
                patient_firstname=item.patient_firstname,
                patient_lastname=item.patient_lastname,
                visit_begin_visit_time=item.visit_begin_visit_time,
                status=item.status
            )
            for item in dto.prescriptions
        ]
    )