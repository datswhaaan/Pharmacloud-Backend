from app.domain.entities.prescription import DetectionItem, OrderDrugItem, Prescription, PrescriptionList
from app.application.dto.prescription_dto import DetectionItemDTO, PrescriptionDTO, PrescriptionItemDTO, PrescriptionListDTO, DetectionDTO

def _to_prescription_dto(prescription: Prescription) -> PrescriptionDTO:
    return PrescriptionDTO(
        visit_id=prescription.t_visit_id,
        visit_hn=prescription.visit_hn,
        visit_vn=prescription.visit_vn,
        f_visit_type=prescription.f_visit_type,
        visit_begin_visit_time=prescription.visit_begin_visit_time,
        visit_diagnosis_notice=prescription.visit_diagnosis_notice,
        visit_patient_type=prescription.visit_patient_type,
        visit_queue=prescription.visit_queue,
        visit_dx=prescription.visit_dx,
        f_patient_prefix=prescription.f_patient_prefix,
        patient_firstname=prescription.patient_firstname,
        patient_lastname=prescription.patient_lastname,
        visit_staff_doctor_discharge=prescription.visit_staff_doctor_discharge,
        visit_deny_allergy=prescription.visit_deny_allergy,
        visit_patient_age=prescription.visit_patient_age,
        risk_factors=prescription.risk_factors,
        order_drugs=prescription.order_drugs
    )

def _to_prescription_list_dto(prescription_list: PrescriptionList) -> PrescriptionListDTO:
    return PrescriptionListDTO(
        prescriptions=[
            PrescriptionItemDTO(
                visit_id=prescription.t_visit_id,
                visit_hn=prescription.visit_hn,
                visit_vn=prescription.visit_vn,
                f_patient_prefix=prescription.f_patient_prefix,
                patient_firstname=prescription.patient_firstname,
                patient_lastname=prescription.patient_lastname,
                visit_begin_visit_time=prescription.visit_begin_visit_time,
                status=prescription.status
            )
            for prescription in prescription_list.prescriptions
        ]
    )

def _to_detection_item_dto(ordered: OrderDrugItem, detected: DetectionItem) -> DetectionItemDTO:
    return DetectionItemDTO(
        t_order_drug_id=ordered.t_order_drug_id,
        detection_item_id=detected.detection_item_id,
        item_common_name=detected.item_common_name,
        confidence=detected.confidence,
        quantity=ordered.quantity,
        unit=ordered.unit
    )

def _to_detection_dto(detection, matched, missing, extra) -> DetectionDTO:
    return DetectionDTO(
        detection_id=detection.detection_id,
        verified_at=str(detection.verified_at),
        verified_by=detection.verified_by,
        matched=matched,
        missing=missing,
        extra=extra
    )
