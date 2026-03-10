from sqlalchemy.orm import Session, selectinload
from app.infrastructure.models.prescription import OrderDrugORM, OrderORM, PatientORM, PatientORM, PrescriptionORM
from app.infrastructure.mappers.prescription_mapper import _to_prescription
from app.domain.entities.prescription import Prescription
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