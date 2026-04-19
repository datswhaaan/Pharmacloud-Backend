from datetime import datetime
from sqlalchemy import case
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.exception.detection import RepositoryError
from app.domain.repositories.detection import DetectionRepository
from app.infrastructure.storage.google_drive_storage import GoogleDriveStorage
from app.domain.entities.detection import DetectionList, Detection, DetectionImageInput
from app.infrastructure.models.detection import DetectionORM, DetectionItemORM, OrderDrugORM
from app.infrastructure.mappers.detection_mapper import _to_detection_list, _to_detection_orm, _to_detection, _to_detection_item_orm

class DetectionRepositoryImpl(DetectionRepository):
    
    def __init__(self, session: Session, google_drive_storage: GoogleDriveStorage):
        self.session = session
        self.storage = google_drive_storage

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

    def create_detection(self, detection: Detection, image: DetectionImageInput) -> Detection:
        file_id = None
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            file_name = f"{detection.t_order_id}_{timestamp}"
            file_id = self.storage.upload(image, file_name)

            detection_image_url = self.storage.get_public_url(file_id)

            detection_orm = _to_detection_orm(detection, detection_image_url)

            self.session.add(detection_orm)
            self.session.flush()
            self.session.refresh(detection_orm)

            detection_list = _to_detection_item_orm(detection.detections, detection_orm.detection_id)
            self.session.add_all(detection_list)
            self.session.commit()
            
        except (IntegrityError, SQLAlchemyError) as e:
            self.session.rollback()
            
            try:
                self.storage.delete(file_id)
            except Exception:
                pass

            raise RepositoryError(f"Database error occurred: {str(e)}")
        return _to_detection(detection_orm)
        