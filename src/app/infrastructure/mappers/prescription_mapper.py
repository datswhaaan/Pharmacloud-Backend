from app.domain.entities.prescription import Prescription, RiskFactor, OrderDrug
from app.infrastructure.models.prescription import PrescriptionORM

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
    return Prescription(
        t_visit_id=orm.t_visit_id,
        visit_hn=orm.visit_hn,
        visit_vn=orm.visit_vn,
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
        order_drugs=_to_order_drug(orm)
    )