from app.domain.entities.prescription import OrderDrugItem, Prescription, RiskFactor, OrderDrug, PrescriptionList, PrescriptionItem, OrderList, PatientHistory, PastHistory, FamilyHistory, DrugAllergy
from app.infrastructure.models.prescription import OrderORM

def _to_risk_factor(orm: OrderDrug) -> list[RiskFactor]:
    return [
        RiskFactor(
            patient_risk_factor_topic=risk_factor.patient_risk_factor_topic,
            patient_risk_factor_description=risk_factor.patient_risk_factor_description
        )
        for risk_factor in orm.visit.patient.risk_factors
    ]

def _to_order_drug(orm: OrderORM) -> list[OrderDrug]:
    return [
        OrderDrug(
            b_item_id=od.item.b_item_id,
            item_common_name=od.item.item_common_name,
            b_item_drug_uom_id_purch=od.item_drug_uom.item_drug_uom_description,
            order_drug_dose=od.order_drug_dose
        )
        for od in orm.order_drugs
    ]

def _to_prescription(orm: OrderORM) -> Prescription:
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

    for da in orm.visit.patient.drug_allergy:
        if not da.item or not da.warning_type:
            continue
        key = mapping.get(da.warning_type.f_allergy_warning_type_id)
        if key:
            result[key].append(da.item.item_common_name)

    return Prescription(
        order_id=orm.t_order_id,
        visit_hn=orm.visit.visit_hn,
        visit_vn=orm.visit.visit_vn,
        status=orm.status.f_order_status_id,
        visit_begin_visit_time=orm.visit.visit_begin_visit_time,
        visit_diagnosis_notice=orm.visit.visit_diagnosis_notice,
        visit_patient_type=orm.visit.visit_patient_type,
        visit_dx=orm.visit.visit_dx,
        f_patient_prefix=orm.visit.patient.prefix.patient_prefix_description,
        patient_firstname=orm.visit.patient.patient_firstname,
        patient_lastname=orm.visit.patient.patient_lastname,
        visit_staff_doctor_discharge=orm.visit.employee.employee_firstname + " " + orm.visit.employee.employee_lastname,
        visit_patient_age=orm.visit.visit_patient_age, 
        risk_factors=_to_risk_factor(orm),
        history=PatientHistory(
            past_history=[
                PastHistory(
                    patient_past_history_topic=ph.patient_past_history_topic
                ) for ph in orm.visit.patient.past_history
            ],
            family_history=[
                FamilyHistory(
                    patient_family_topic=fh.patient_family_topic
                ) for fh in orm.visit.patient.family_history
            ]
        ),
        drug_allergy = DrugAllergy(**result),
        payment = orm.visit.payment[0].contract.contract_plans_description,
        symptom = (
            orm.visit.symptom[0].visit_primary_symptom_main_symptom
            + " ("
            + orm.visit.symptom[0].staff_record.employee_firstname
            + " "
            + orm.visit.symptom[0].staff_record.employee_lastname
            + " บันทึก)"
        )
    )

def _to_prescription_list(orms: list[OrderORM], total: int, page: int, size: int) -> PrescriptionList:
    return PrescriptionList(
        prescriptions=[
            PrescriptionItem(
                order_id=orm.t_order_id,
                visit_hn=orm.visit_hn,
                visit_vn=orm.visit_vn,
                f_patient_prefix=orm.patient_prefix_description,
                patient_firstname=orm.patient_firstname,
                patient_lastname=orm.patient_lastname,
                visit_begin_visit_time=orm.visit_begin_visit_time,
                status = orm.f_order_status_id,
                verified_by=None
            )
            for orm in orms
        ],
        total=total,
        page=page,
        size=size
    )

def _to_order_list(orms: list[OrderORM]) -> OrderList:
    return OrderList(
        orders=[
            OrderDrugItem(
                t_order_drug_id=od.t_order_drug_id,
                b_item_id=od.item.b_item_id,
                item_common_name=od.item.item_common_name,
                unit=od.item_drug_uom.item_drug_uom_description,
                quantity=od.order_drug_dose
            )
            for orm in orms
            for od in orm.order_drugs
        ]
    )