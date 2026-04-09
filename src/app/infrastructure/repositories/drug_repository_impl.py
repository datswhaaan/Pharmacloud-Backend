from datetime import datetime
from sqlalchemy import func, case
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infrastructure.models.drug import DrugInstructionORM, DrugORM, DrugImageORM, ImageVariantORM
from app.domain.exception.drug import RepositoryError, DrugNotFoundError
from app.domain.entities.drug import Drug, DrugImage, DrugImageList, DrugList, ImageVariantList, DrugImageListUpload
from app.domain.repositories.drug import DrugRepository
from app.infrastructure.mappers.drug_mapper import _to_drug, _to_drug_list, _to_drug_image_orm, to_image_variant_list, _to_drug_image
from app.infrastructure.storage.google_drive_storage import GoogleDriveStorage
from googleapiclient.errors import HttpError

class DrugRepositoryImpl(DrugRepository):
    def __init__(
            self, 
            session: Session, 
            google_drive_storage: GoogleDriveStorage
        ):
        self.session = session
        self.storage = google_drive_storage

    def get_by_id(self, id: str) -> Drug | None:
        row = (
            self.session
            .query(DrugORM)
            .options(
                selectinload(DrugORM.images)
                    .selectinload(DrugImageORM.variant),
                selectinload(DrugORM.instructions),
                selectinload(DrugORM.subgroup),
                selectinload(DrugORM.billing_subgroup),
                selectinload(DrugORM.group_16)
            )
            .filter(DrugORM.b_item_id == id)
            .first()
        )

        if row is None:
            raise DrugNotFoundError(
                f"Drug with id: {id} not found"
            )
        
        return _to_drug(row)

    def get_all(
        self,
        search: str | None = None,
        *,
        high_alert: bool,
        skip: int = 0,
        limit: int = 100
    ) -> DrugList:
        
        high_alert_subq = (
            self.session.query(
                DrugInstructionORM.b_item_id,
                func.max(
                    case(
                        (DrugInstructionORM.height_alert == "Y", 1),
                        else_=0
                    )
                ).label("has_high_alert")
            )
            .group_by(DrugInstructionORM.b_item_id)
            .subquery()
        )

        image_count_subq = (
            self.session.query(
                DrugImageORM.b_item_id,
                func.count(DrugImageORM.drug_image_id).label("image_count")
            )
            .group_by(DrugImageORM.b_item_id)
            .subquery()
        )

        query = (
            self.session.query(
                DrugORM.b_item_id,
                DrugORM.item_number,
                DrugORM.item_common_name,
                func.coalesce(high_alert_subq.c.has_high_alert, 0).label("is_high_alert"),
                func.coalesce(image_count_subq.c.image_count, 0).label("image_count")
            )
            .join(
                high_alert_subq,
                DrugORM.b_item_id == high_alert_subq.c.b_item_id
            )
            .outerjoin(
                image_count_subq, 
                DrugORM.b_item_id == image_count_subq.c.b_item_id
            )
        )

        if search:
            query = query.filter(
                DrugORM.item_common_name.ilike(f"%{search}%") |
                DrugORM.b_item_id.ilike(f"%{search}%") |
                DrugORM.item_trade_name.ilike(f"%{search}%") |
                DrugORM.item_nick_name.ilike(f"%{search}%") |
                DrugORM.item_number.ilike(f"%{search}%")
            )

        if high_alert:
            query = query.filter(
                high_alert_subq.c.has_high_alert == 1
            )

        rows = (
            query
            .order_by(func.coalesce(image_count_subq.c.image_count, 0).asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        total = (
            query
            .count()
        )

        page = (skip // limit) + 1 if limit else 1

        return _to_drug_list(rows, total, page, min(limit, total - skip))
    
    def add_drug_image(self, drug_id: str, trade_name: str, images: DrugImageListUpload) -> DrugImageList:
        uploaded_files = []
        created_images = []

        try:
            drug = self.session.query(DrugORM).filter(DrugORM.b_item_id == drug_id).first()

            if not drug:
                raise DrugNotFoundError(f"Drug with id: {drug_id} not found")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for image in images.images:
                file_name = f"{drug_id}_{trade_name}_{image.view_type}_{image.position}_{image.lighting}_{timestamp}"
                file_id = self.storage.upload(image, file_name)
                uploaded_files.append(file_id)
                
                drug_image_url = self.storage.get_public_url(file_id)

                orm = _to_drug_image_orm(drug_id, image, drug_image_url, file_id)

                self.session.add(orm)
                self.session.flush()

                created_images.append(_to_drug_image(orm))

            self.session.commit()

        except (IntegrityError, SQLAlchemyError) as e:
            self.session.rollback()

            for file_id in uploaded_files:
                try:
                    self.storage.delete(file_id)
                except Exception:
                    pass

            raise RepositoryError(f"Database error occurred: {str(e)}")
        return DrugImageList(
            b_item_id = drug_id,
            images = created_images
        )

    def delete_drug_image(self, image_ids: list[str]) -> None:
        try:
            images = (
                self.session.query(DrugImageORM)
                .filter(DrugImageORM.drug_image_id.in_(image_ids))
                .all()
            )

            if not images:
                raise DrugNotFoundError(f"Image with ids: {image_ids} not found")

            
            for img in images:
                try:
                    self.storage.delete(file_id=img.file_id)
                except HttpError as e:
                    if e.resp.status != 404:
                        raise
            
            (
                self.session.query(DrugImageORM)
                .filter(DrugImageORM.drug_image_id.in_(image_ids))
                .delete(synchronize_session=False)
            )
            self.session.commit()

        except (IntegrityError, SQLAlchemyError) as e:
            self.session.rollback()
            raise RepositoryError(f"Database error occurred: {str(e)}")
        
    def get_variant_map(self) -> ImageVariantList:
        try:
            rows = self.session.query(ImageVariantORM).all()
            return to_image_variant_list(rows)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"Database error occurred: {str(e)}")