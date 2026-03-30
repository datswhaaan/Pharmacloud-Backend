from sqlalchemy import case
from sqlalchemy.orm import Session, selectinload
from app.infrastructure.models.prescription import OrderDrugORM, OrderORM, PatientORM, PatientORM, PrescriptionORM, PatientPrefixORM, OrderStatusORM, DetectionORM, DetectionItemORM
from app.infrastructure.mappers.prescription_mapper import _to_prescription, _to_prescription_list, _to_detection_list, _to_order_list
from app.domain.entities.prescription import Prescription, PrescriptionList, DetectionList, OrderList
from app.domain.exception.prescription import PrescriptionNotFoundException

class PrescriptionRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session

    def get_prescription_by_id(self, id: str) -> Prescription:
        row = (
            self.session
            .query(PrescriptionORM)
            .options(
                selectinload(PrescriptionORM.visit_type),
                selectinload(PrescriptionORM.patient)
                    .selectinload(PatientORM.prefix),
                selectinload(PrescriptionORM.patient)
                    .selectinload(PatientORM.risk_factors),
                selectinload(PrescriptionORM.employee),
                selectinload(PrescriptionORM.orders)
                    .selectinload(OrderORM.order_drugs)
                    .selectinload(OrderDrugORM.item_drug_uom),
                selectinload(PrescriptionORM.orders)
                    .selectinload(OrderORM.item)
            )
            .filter(
                PrescriptionORM.t_visit_id == id
            )
            .first()
        )

        if row is None:
            raise PrescriptionNotFoundException(
                f"Prescription with id: {id} not found"
            )
        
        return _to_prescription(row)

    def get_all_prescriptions(self, start_time: str, end_time: str, limit: int, skip: int, order: str) -> PrescriptionList:
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
        
        query = self.session.query(
            PrescriptionORM.t_visit_id,
            PrescriptionORM.visit_hn,
            PrescriptionORM.visit_vn,
            PatientPrefixORM.patient_prefix_description,
            PatientORM.patient_firstname,
            PatientORM.patient_lastname,
            PrescriptionORM.visit_begin_visit_time,
            OrderStatusORM.f_order_status_id
        )
        
        rows = (
            query
            .join(PrescriptionORM.patient)
            .join(PrescriptionORM.orders)
            .join(OrderORM.status)
            .join(PatientORM.prefix)
            .filter(
                PrescriptionORM.visit_begin_visit_time >= start_time if start_time else True,
                PrescriptionORM.visit_begin_visit_time <= end_time if end_time else True
            )
            .order_by(
                status_order,
                PrescriptionORM.visit_begin_visit_time.asc() if order == "asc" 
                else PrescriptionORM.visit_begin_visit_time.desc()
            )
            .limit(limit)
            .offset(skip)
            .all()
        )

        total = (
            self.session.query(PrescriptionORM.t_visit_id)
            .join(PrescriptionORM.patient)
            .join(PrescriptionORM.orders)
            .join(OrderORM.status)
            .filter(
                PrescriptionORM.visit_begin_visit_time >= start_time if start_time else True,
                PrescriptionORM.visit_begin_visit_time <= end_time if end_time else True
            )
            .count()
        )

        page = (skip // limit) + 1 if limit else 1

        return _to_prescription_list(rows, total, page, limit)

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
                selectinload(DetectionORM.employee)
            )
            .filter(
                DetectionORM.t_order_id == order_id
            )
            .order_by(DetectionORM.verified_at.desc())
            .all()
        )

        return _to_detection_list(rows)