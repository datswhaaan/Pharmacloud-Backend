from app.domain.entities.prescription import OrderDrugItem, Prescription, RiskFactor, OrderDrug, PrescriptionList, PrescriptionItem, DetectionItem, DetectionList, Detection, OrderList, PatientHistory, PastHistory, FamilyHistory, DrugAllergy
from app.infrastructure.models.prescription import PrescriptionORM, DetectionORM, OrderORM

def _to_risk_factor(orm: PrescriptionORM) -> list[RiskFactor]:
    return [
        RiskFactor(
            patient_risk_factor_topic=risk_factor.patient_risk_factor_topic,
            patient_risk_factor_description=risk_factor.patient_risk_factor_description
        )
        for risk_factor in orm.patient.risk_factors
    ]

def _to_order_drug(orm: PrescriptionORM) -> list[OrderDrug]:
    return [
        OrderDrug(
            b_item_id=od.item.b_item_id,
            item_common_name=od.item.item_common_name,
            b_item_drug_uom_id_purch=od.item_drug_uom.item_drug_uom_description,
            order_drug_dose=od.order_drug_dose
        )
        for order in orm.orders
        for od in order.order_drugs
    ]


def _to_prescription(orm: PrescriptionORM) -> Prescription:
    mapping = {
        "1": "drug_allergies",
        "2": "monitoring",
        "3": "suspected"
    }

    result = {
        "drug_allergies": [],
        "monitoring": [],
        "suspected": []
    }

    for da in orm.patient.drug_allergy:
        if not da.item or not da.warning_type:
            continue
        key = mapping.get(da.warning_type.f_allergy_warning_type_id)
        if key:
            result[key].append(da.item.item_common_name)

    return Prescription(
        t_visit_id=orm.t_visit_id,
        visit_hn=orm.visit_hn,
        visit_vn=orm.visit_vn,
        status=orm.orders[0].status.f_order_status_id,
        f_visit_type=orm.visit_type.visit_type_description,
        visit_begin_visit_time=orm.visit_begin_visit_time,
        visit_diagnosis_notice=orm.visit_diagnosis_notice,
        visit_patient_type=orm.visit_patient_type,
        visit_queue=orm.visit_queue,
        visit_dx=orm.visit_dx,
        f_patient_prefix=orm.patient.prefix.patient_prefix_description,
        patient_firstname=orm.patient.patient_firstname,
        patient_lastname=orm.patient.patient_lastname,
        visit_staff_doctor_discharge=orm.employee.employee_firstname + " " + orm.employee.employee_lastname,
        visit_deny_allergy=orm.visit_deny_allergy,
        visit_patient_age=orm.visit_patient_age, 
        risk_factors=_to_risk_factor(orm),
        order_drugs=_to_order_drug(orm),
        history=PatientHistory(
            past_history=[
                PastHistory(
                    patient_past_history_topic=ph.patient_past_history_topic
                ) for ph in orm.patient.past_history
            ],
            family_history=[
                FamilyHistory(
                    patient_family_topic=fh.patient_family_topic
                ) for fh in orm.patient.family_history
            ]
        ),
        drug_allergy = DrugAllergy(**result)
    )

def _to_prescription_list(orms: list[PrescriptionORM], total: int, page: int, size: int) -> PrescriptionList:
    return PrescriptionList(
        prescriptions=[
            PrescriptionItem(
                t_visit_id=orm.t_visit_id,
                visit_hn=orm.visit_hn,
                visit_vn=orm.visit_vn,
                f_patient_prefix=orm.patient_prefix_description,
                patient_firstname=orm.patient_firstname,
                patient_lastname=orm.patient_lastname,
                visit_begin_visit_time=orm.visit_begin_visit_time,
                status = orm.f_order_status_id
            )
            for orm in orms
        ],
        total=total,
        page=page,
        size=size
    )

def _to_detection_list(orms: list[DetectionORM]) -> DetectionList:
    return DetectionList(
        detections=[
            Detection(
                detection_id=orm.detection_id,
                detected_at=orm.detected_at,
                image_url=orm.image_url,
                verified_by=orm.employee.employee_firstname + " " + orm.employee.employee_lastname,
                verified_at=orm.verified_at,
                detections=[
                    DetectionItem(
                        detection_item_id=di.detection_item_id,
                        b_item_id=di.b_item_id,
                        item_common_name=di.item.item_common_name,
                        confidence=di.confidence
                    )
                    for di in orm.detection_item
                ]
            ) for orm in orms
        ]
    )

def _to_order_list(orms: list[OrderORM]) -> OrderList:
    return OrderList(
        orders=[
            OrderDrugItem(
                t_order_drug_id=od.t_order_id,
                b_item_id=od.item.b_item_id,
                item_common_name=od.item.item_common_name,
                unit=od.item_drug_uom.item_drug_uom_description,
                quantity=od.order_drug_dose
            )
            for orm in orms
            for od in orm.order_drugs
        ]
    )