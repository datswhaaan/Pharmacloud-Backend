from datetime import datetime
from sqlalchemy import case
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.exception.detection import RepositoryError
from app.domain.repositories.detection import DetectionRepository
from app.infrastructure.storage.google_drive_storage import GoogleDriveStorage
from app.domain.entities.detection import DetectionList, Detection, DetectionImageInput, DetectionCreate, DetectionUpdate
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
                selectinload(DetectionORM.employee)
            )
            .filter(
                DetectionORM.t_order_id == order_id,
                DetectionORM.status != "UNVERIFIED"
            )
            .order_by(DetectionORM.verified_at.desc())
            .all()
        )

        return _to_detection_list(rows)
    
    def get_detections_by_detection_id(self, detection_id: str) -> DetectionList:
        row = (
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
                DetectionORM.detection_id == detection_id
            )
            .order_by(DetectionORM.verified_at.desc())
            .first()
        )

        return _to_detection(row)

    def create_detection(self, detection: DetectionCreate, image: DetectionImageInput) -> Detection:
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
    
    def update_detection(self, detection: DetectionUpdate) -> Detection:
        try:
            detection_orm = (
                self.session.query(DetectionORM)
                .filter(DetectionORM.detection_id == detection.detection_id)
                .first()
            )

            if not detection_orm:
                raise RepositoryError(
                    f"Detection with ID {detection.detection_id} not found"
                )

            detection_orm.status = detection.status
            detection_orm.verified_by = detection.verified_by
            detection_orm.verified_at = detection.verified_at

            detection_items_orm = (
                self.session.query(DetectionItemORM)
                .filter(DetectionItemORM.detection_id == detection.detection_id)
                .all()
            )

            dto_map = {
                item.detection_item_id: item
                for item in detection.drug_list
            }

            for item_orm in detection_items_orm:
                dto = dto_map.get(item_orm.detection_item_id)
                if not dto:
                    continue

                item_orm.quantity = dto.quantity
                item_orm.is_manually_edited = dto.is_manually_edited
                item_orm.match_type = dto.match_type
                item_orm.error_type = dto.error_type

            self.session.commit()
            self.session.refresh(detection_orm)

        except (IntegrityError, SQLAlchemyError) as e:
            self.session.rollback()
            raise RepositoryError(f"Database error occurred: {str(e)}")

        return _to_detection(detection_orm)