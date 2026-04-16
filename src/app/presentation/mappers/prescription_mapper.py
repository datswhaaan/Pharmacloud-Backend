
from app.application.dto.prescription_dto import PrescriptionDTO, PrescriptionListDTO, DetectionListDTO
from app.presentation.schemas.prescription_response import PrescriptionItemResponse, PrescriptionListResponse, PrescriptionListResponse, PrescriptionDetailResponse, RiskFactorResponse, OrderDrugResponse, DetectionListResponse, DetectionItemResponse, DetectionResponse, PatientHistoryResponse, DrugAllergyResponse

def _to_prescription_response(dto: PrescriptionDTO) -> PrescriptionDetailResponse:

    risk_factors = RiskFactorResponse(
            alcoholUse=dto.risk_factors.alcoholUse,
            smokingHabits=dto.risk_factors.smokingHabits
        )

    history = PatientHistoryResponse(
        past_history=[ph.patient_past_history_topic for ph in dto.history.past_history],
        family_history=[fh.patient_family_history_topic for fh in dto.history.family_history]
    )

    return PrescriptionDetailResponse(
        order_id=dto.order_id,
        visit_hn=dto.visit_hn,
        visit_vn=dto.visit_vn,
        status=dto.status,
        visit_begin_visit_time=dto.visit_begin_visit_time,
        visit_diagnosis_notice=dto.visit_diagnosis_notice,
        visit_patient_type=dto.visit_patient_type,
        visit_dx=dto.visit_dx,
        patient_name=dto.patient_name,
        visit_staff_doctor_discharge=dto.visit_staff_doctor_discharge,
        visit_patient_age=dto.visit_patient_age,
        risk_factors=risk_factors,
        history=history,
        drug_allergy=DrugAllergyResponse(
            drug_allergies=dto.drug_allergy.drug_allergies,
            monitoring=dto.drug_allergy.monitoring,
            suspected=dto.drug_allergy.suspected
        ),
        payment=dto.payment,
        symptom=dto.symptom
    )

def _to_prescription_list_response(dto: PrescriptionListDTO) -> PrescriptionListResponse:
    return PrescriptionListResponse(
        prescriptions=[
            PrescriptionItemResponse(
                order_id=item.order_id,
                visit_hn=item.visit_hn,
                visit_vn=item.visit_vn,
                patient_name=item.f_patient_prefix + item.patient_firstname + " " + item.patient_lastname,
                visit_begin_visit_time=item.visit_begin_visit_time,
                status=item.status,
                verified_by=item.verified_by
            )
            for item in dto.prescriptions
        ],
        total=dto.total,
        page=dto.page,
        size=dto.size
    )

def _to_detection_list_response(dto: DetectionListDTO) -> DetectionListResponse:
    return DetectionListResponse(
        order_drugs=[
            OrderDrugResponse(
                t_order_drug_id=od.t_order_drug_id,
                item_common_name=od.item_common_name,
                unit=od.unit,
                quantity=od.quantity
            ) for od in dto.order_drugs
        ],
        detections=[
            DetectionResponse(
                detection_id=d.detection_id,
                image_url=d.image_url,
                status=d.status,
                verified_by=d.verified_by,
                verified_at=d.verified_at,
                drug_list=[
                    DetectionItemResponse(
                        t_order_drug_id=drug.t_order_drug_id,
                        detection_item_id=drug.detection_item_id,
                        item_common_name=drug.item_common_name,
                        confidence=drug.confidence,
                        confidence_level=drug.confidence_level,
                        quantity=drug.quantity,
                        unit=drug.unit,
                        is_manually_edited=drug.is_manually_edited,
                        match_type=drug.match_type
                    ) for drug in d.drug_list 
                ]
            )
            for d in dto.detections
        ]
    )