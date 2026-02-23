from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infrastructure.models.drug import DrugORM, DrugImageORM, ImageVariantORM
from app.domain.exception.drug import RepositoryError, DrugNotFoundError
from app.domain.entities.drug import Drug, DrugList
from app.domain.repositories.drug import DrugRepository
from app.infrastructure.mappers.drug_mapper import _to_drug, _to_drug_list, _to_drug_orm

class DrugRepositoryImpl(DrugRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: str) -> Drug | None:
        row = (
            self.session
            .query(DrugORM)
            .options(
                selectinload(DrugORM.images)
                .selectinload(DrugImageORM.variant)
                .selectinload(DrugORM.instructions)
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
        *,
        skip: int = 0,
        limit: int = 100
    ) -> DrugList:
        
        rows = (
            self.session
            .query(DrugORM)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return _to_drug_list(rows)

    def update(self, drug: Drug) -> Drug:
        row = (
            self.session
            .query(DrugORM)
            .filter(DrugORM.b_item_id == drug.b_item_id)
            .first()
        )

        if row is None:
            raise DrugNotFoundError(
                f"Item with id {drug.b_item_id} not found"
            )
        
        for key, value in vars(drug).items():
            if value is not None:
                setattr(row, key, value)
        
        try:
            self.session.commit()
            self.session.refresh(row)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(str(e))

        return row 