from sqlalchemy import case
from sqlalchemy.orm import Session, selectinload
from app.infrastructure.models.prescription import OrderDrugORM, OrderORM, PatientORM, PatientORM, VisitORM, PatientPrefixORM, OrderStatusORM, DetectionORM, DetectionItemORM, PatientDrugAllergyORM, PaymentORM, SymptomORM, EmployeeORM
from app.infrastructure.mappers.prescription_mapper import _to_prescription, _to_prescription_list, _to_detection_list, _to_order_list
from app.domain.entities.prescription import Prescription, PrescriptionList, DetectionList, OrderList
from app.domain.exception.prescription import PrescriptionNotFoundException

class PrescriptionRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session

    def get_prescription_by_id(self, id: str) -> Prescription:
        row = (
            self.session
            .query(OrderORM)
            .options(
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.visit_type),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.patient)
                    .selectinload(PatientORM.prefix),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.patient)
                    .selectinload(PatientORM.risk_factors),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.patient)
                    .selectinload(PatientORM.past_history),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.patient)
                    .selectinload(PatientORM.family_history),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.patient)
                    .selectinload(PatientORM.drug_allergy)
                    .selectinload(PatientDrugAllergyORM.item),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.employee),
                selectinload(OrderORM.order_drugs)
                    .selectinload(OrderDrugORM.item_drug_uom),
                selectinload(OrderORM.item),
                selectinload(OrderORM.status),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.payment)
                    .selectinload(PaymentORM.contract),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.symptom)
                    .selectinload(SymptomORM.staff_record),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.symptom)
                    .selectinload(SymptomORM.staff_modify),
                selectinload(OrderORM.visit)
                    .selectinload(VisitORM.symptom)
                    .selectinload(SymptomORM.staff_cancel)
            )
            .filter(
                OrderORM.t_order_id == id
            )
            .first()
        )

        if row is None:
            raise PrescriptionNotFoundException(
                f"Prescription with id: {id} not found"
            )
        
        return _to_prescription(row)

    def get_all_prescriptions(
            self, 
            start_time: str, 
            end_time: str, 
            limit: int, skip: int, order: str,
            status: list[str],
            search: str | None = None
    ) -> PrescriptionList:
        STATUS_PRIORITY = {
            '1': 2,  # ยืนยัน
            '2': 1,  # ดำเนินการ
            '6': 2,  # ค้างรายงานผล
            '4': 1,  # รายงานผล
            '3': 2,  # จ่าย
            '5': 3   # ยกเลิก
        }

        status_order = case(
            STATUS_PRIORITY,
            value=OrderStatusORM.f_order_status_id,
            else_=999
        )
        
        query = (
            self.session.query(
                OrderORM.t_order_id,
                VisitORM.visit_hn,
                VisitORM.visit_vn,
                PatientPrefixORM.patient_prefix_description,
                PatientORM.patient_firstname,
                PatientORM.patient_lastname,
                VisitORM.visit_begin_visit_time,
                OrderStatusORM.f_order_status_id,
                EmployeeORM.employee_firstname,
                EmployeeORM.employee_lastname
                
            )
            .join(OrderORM.visit)
            .join(VisitORM.patient)
            .join(PatientORM.prefix)
            .join(OrderORM.status)
            .join(OrderORM.detection)
            .join(DetectionORM.employee)
        )
        
        if search:
            query = query.filter(
                VisitORM.visit_hn.ilike(f"%{search}%") |
                VisitORM.visit_vn.ilike(f"%{search}%") |
                PatientORM.patient_firstname.ilike(f"%{search}%") |
                PatientORM.patient_lastname.ilike(f"%{search}%")
            )

        if len(status) > 0:
            query = query.filter(
                OrderStatusORM.f_order_status_id.in_(status)
            )

        if start_time:
            query = query.filter(VisitORM.visit_begin_visit_time >= start_time)

        if end_time:
            query = query.filter(VisitORM.visit_begin_visit_time <= end_time)
        
        rows = (
            query
            .order_by(
                status_order,
                VisitORM.visit_begin_visit_time.asc()
                if order == "asc"
                else VisitORM.visit_begin_visit_time.desc()
            )
            .limit(limit)
            .offset(skip)
            .all()
        )

        total = (
            self.session.query(VisitORM.t_visit_id)
            .join(VisitORM.patient)
            .join(VisitORM.orders)
            .join(OrderORM.status)
            .count()
        )

        page = (skip // limit) + 1 if limit else 1

        return _to_prescription_list(rows, total, page, min(limit, total - skip))

    def get_orders_by_order_id(self, order_id: str) -> OrderList:
        rows = (
            self.session
            .query(OrderORM)
            .options(
                selectinload(OrderORM.order_drugs)
                    .selectinload(OrderDrugORM.item_drug_uom),
                selectinload(OrderORM.item)
            )
            .filter(
                OrderORM.t_order_id == order_id
            )
            .all()
        )

        return _to_order_list(rows)

    def get_detections_by_order_id(self, order_id: str) -> DetectionList:
        
        rows = (
            self.session
            .query(DetectionORM)
            .options(
                selectinload(DetectionORM.detection_item)
                    .selectinload(DetectionItemORM.order_drugs)
                    .selectinload(OrderDrugORM.item_drug_uom),
                selectinload(DetectionORM.detection_item)
                    .selectinload(DetectionItemORM.item),
                selectinload(DetectionORM.orders),
                selectinload(DetectionORM.employee),
                selectinload(DetectionORM.detection_status)
            )
            .filter(
                DetectionORM.t_order_id == order_id
            )
            .order_by(DetectionORM.verified_at.desc())
            .all()
        )

        return _to_detection_list(rows)