from app.domain.entities.prescription import DetectionItem, OrderDrugItem, Prescription, PrescriptionList, RiskFactor, OrderList, Detection
from app.application.dto.prescription_dto import DetectionItemDTO, PrescriptionDTO, PrescriptionItemDTO, PrescriptionListDTO, DetectionDTO, RiskFactorDTO, PatientHistoryDTO, PastHistoryDTO, FamilyHistoryDTO, DrugAllergyDTO, DetectionListDTO, OrderDrugDTO

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
                status=_status_mapper(prescription.status)
            )
            for prescription in prescription_list.prescriptions
        ],
        total=prescription_list.total,
        page=prescription_list.page,
        size=prescription_list.size
    )

def _to_detection_item_dto(
    ordered: OrderDrugItem | None,
    detected: DetectionItem | None,
    match_type: str
) -> DetectionItemDTO:
    return DetectionItemDTO(
        t_order_drug_id=ordered.t_order_drug_id if ordered else "",
        detection_item_id=detected.detection_item_id if detected else "",
        item_common_name=ordered.item_common_name if ordered else detected.item_common_name,
        confidence=detected.confidence if detected else "0",
        confidence_level=_confidence_level_mapper(detected.confidence) if detected else "",
        quantity=detected.quantity if detected else ordered.quantity,
        unit=ordered.unit if ordered else detected.unit,
        is_manually_edited=detected.is_manually_edited if detected else False,
        match_type=match_type
    )

def _to_detection_dto(detection: Detection, drug_list: list[DetectionItemDTO]) -> DetectionDTO:
    return DetectionDTO(
        detection_id=detection.detection_id,
        image_url=detection.image_url,
        status=detection.status,
        verified_at=str(detection.verified_at),
        verified_by=detection.verified_by,
        drug_list=drug_list
    )

def _to_detection_list_dto(order_list: OrderList, detection_list: list[DetectionItemDTO]) -> DetectionListDTO:
    return DetectionListDTO(
        order_drugs=[
            OrderDrugDTO(
                t_order_drug_id=od.t_order_drug_id,
                item_common_name=od.item_common_name,
                unit=od.unit,
                quantity=od.quantity
            ) for od in order_list.orders
        ],
        detections=detection_list
    )

def _status_mapper(status_id: str) -> str:
    mapping = {
        '1': "completed",
        '2': "waiting",
        '6': "completed",
        '4': "waiting",
        '3': "completed",
        '5': "cancelled"
    }
    return mapping.get(status_id, "unknown")


def _confidence_level_mapper(confidence_level: float) -> str:
    if confidence_level >= 80:
        return "High"
    elif confidence_level >=60:
        return "Medium"
    else: return "Low"