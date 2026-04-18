from sqlalchemy import case
from sqlalchemy.orm import Session, selectinload
from app.domain.repositories.detection import DetectionRepository
from app.domain.entities.detection import DetectionList
from app.infrastructure.models.detection import DetectionORM, DetectionItemORM, OrderDrugORM
from app.infrastructure.mappers.detection_mapper import _to_detection_list

class DetectionRepositoryImpl(DetectionRepository):
    
    def __init__(self, session: Session):
        self.session = session

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