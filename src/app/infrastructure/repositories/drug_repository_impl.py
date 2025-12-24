from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.infrastructure.models.drug import DrugORM
from app.domain.exception.drug import DrugAlreadyExistsError, RepositoryError, DrugNotFoundError
from app.domain.entities.drug import Drug, DrugList
from app.domain.repositories.drug import DrugRepository
from app.infrastructure.mappers.drug_mapper import _to_drug, _to_drug_list, _to_drug_orm

class DrugRepositoryImpl(DrugRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_drug_code(self, drug_code: str) -> Drug | None:
        row = (
            self.session
            .query(DrugORM)
            .filter(DrugORM.drug_code == drug_code)
            .first()
        )

        if row is None:
            raise DrugNotFoundError(
                f"Drug with code {drug_code} not found"
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
    
    def create(self, drug: Drug) -> Drug:
        orm = _to_drug_orm(drug)

        try:
            self.session.add(orm)
            self.session.commit()
            return drug
        except IntegrityError:
            self.session.rollback()
            raise DrugAlreadyExistsError(
                f"Drug with code {drug.drug_code} already exists"
            )
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(str(e))
        

    def update(self, drug: Drug) -> Drug:
        row = (
            self.session
            .query(DrugORM)
            .filter(DrugORM.drug_code == drug.drug_code)
            .first()
        )

        if row is None:
            raise DrugNotFoundError(
                f"Drug with id {drug.drug_code} not found"
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

    def delete(self, drug_code: str) -> None:
        orm = (
            self.session
            .query(DrugORM)
            .filter(DrugORM.drug_code == drug_code)
            .first()
        )

        if orm:
            self.session.delete(orm)
            self.session.commit()
        
        return