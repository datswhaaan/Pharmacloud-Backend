
from app.application.dto.prescription_dto import PrescriptionDTO, PrescriptionListDTO, DetectionListDTO
from app.presentation.schemas.prescription_response import PrescriptionItemResponse, PrescriptionListResponse, PrescriptionListResponse, PrescriptionResponse, RiskFactorResponse, OrderDrugResponse, DetectionListResponse, DetectionItemResponse, DetectionResponse, PatientHistoryResponse

def _to_prescription_response(dto: PrescriptionDTO) -> PrescriptionResponse:

    risk_factors = RiskFactorResponse(
            alcoholUse=dto.risk_factors.alcoholUse,
            smokingHabits=dto.risk_factors.smokingHabits
        )

    order_drugs = [
        OrderDrugResponse(
            b_item_id=od.b_item_id,
            item_common_name=od.item_common_name,
            unit=od.b_item_drug_uom_id_purch,
            dose=od.order_drug_dose
        )
        for od in dto.order_drugs
    ]

    history = PatientHistoryResponse(
        past_history=[ph.patient_past_history_topic for ph in dto.history.past_history],
        family_history=[fh.patient_family_history_topic for fh in dto.history.family_history]
    )

    return PrescriptionResponse(
        visit_id=dto.visit_id,
        visit_hn=dto.visit_hn,
        visit_vn=dto.visit_vn,
        status=dto.status,
        f_visit_type=dto.f_visit_type,
        visit_begin_visit_time=dto.visit_begin_visit_time,
        visit_diagnosis_notice=dto.visit_diagnosis_notice,
        visit_patient_type=dto.visit_patient_type,
        visit_queue=dto.visit_queue,
        visit_dx=dto.visit_dx,
        patient_name=dto.f_patient_prefix + dto.patient_firstname + " " + dto.patient_lastname,
        visit_staff_doctor_discharge=dto.visit_staff_doctor_discharge,
        visit_deny_allergy=dto.visit_deny_allergy,
        visit_patient_age=dto.visit_patient_age,
        risk_factors=risk_factors,
        order_drugs=order_drugs,
        history=history
    )

def _to_prescription_list_response(dto: PrescriptionListDTO) -> PrescriptionListResponse:
    return PrescriptionListResponse(
        prescriptions=[
            PrescriptionItemResponse(
                visit_id=item.visit_id,
                visit_hn=item.visit_hn,
                visit_vn=item.visit_vn,
                patient_name=item.f_patient_prefix + item.patient_firstname + " " + item.patient_lastname,
                visit_begin_visit_time=item.visit_begin_visit_time,
                status=item.status
            )
            for item in dto.prescriptions
        ],
        total=dto.total,
        page=dto.page,
        size=dto.size
    )

def _to_detection_list_response(dto: DetectionListDTO) -> DetectionListResponse:
    return DetectionListResponse(
        detections=[
            DetectionResponse(
                detection_id=d.detection_id,
                verified_by=d.verified_by,
                verified_at=d.verified_at,
                matched=[
                    DetectionItemResponse(
                        t_order_drug_id=item.t_order_drug_id,
                        detection_item_id=item.detection_item_id,
                        item_common_name=item.item_common_name,
                        confidence=item.confidence,
                        quantity=item.quantity,
                        unit=item.unit
                    )
                    for item in d.matched
                ],
                missing=[
                    DetectionItemResponse(
                        detection_item_id=item.detection_item_id,
                        item_common_name=item.item_common_name,
                        confidence=item.confidence,
                        quantity=item.quantity,
                        unit=item.unit
                    )
                    for item in d.missing
                ],
                extra=[
                    DetectionItemResponse(
                        detection_item_id=item.detection_item_id,
                        item_common_name=item.item_common_name,
                        confidence=item.confidence,
                        quantity=item.quantity,
                        unit=item.unit
                    )
                    for item in d.extra
                ]
            )
            for d in dto.detections
        ]
    )