from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infrastructure.models.drug import DrugInstructionORM, DrugORM, DrugImageORM
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
        search: str | None = None,
        *,
        high_alert: bool,
        skip: int = 0,
        limit: int = 100
    ) -> DrugList:
        
        rows = (
            self.session
            .query(DrugORM)
            .filter(
                DrugORM.item_common_name.ilike(f"%{search}%")
                | DrugORM.b_item_id.ilike(f"%{search}%")
                | DrugORM.item_trade_name.ilike(f"%{search}%")
                | DrugORM.item_nick_name.ilike(f"%{search}%")
                | DrugORM.item_number.ilike(f"%{search}%")
            ) if search else True
            .filter(
                DrugInstructionORM.height_alert == "Y"
            ) if high_alert else True
            .offset(skip)
            .limit(limit)
            .all()
        )

        return _to_drug_list(rows)