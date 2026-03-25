from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.repositories.user import UserRepository
from app.infrastructure.models.user import EmployeeORM
from app.infrastructure.mappers.user_mapper import _to_user
from app.domain.exception.user import UserNotFoundException
from app.domain.entities.user import User

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: str) -> User:
        row = (
            self.session
            .query(EmployeeORM)
            .options(
                selectinload(EmployeeORM.level),
                selectinload(EmployeeORM.rule),
                selectinload(EmployeeORM.authentication)
            )
            .filter(
                EmployeeORM.employee_active == "1",
                EmployeeORM.b_employee_id == user_id
            )
            .first()
        )
            
        if row is None:
            raise UserNotFoundException(
                f"Prescription with id: {id} not found"
            )
        
        return _to_user(row)

    def get_user_by_username(self, username: str) -> User:
            row = (
                self.session
                .query(EmployeeORM)
                .options(
                    selectinload(EmployeeORM.level),
                    selectinload(EmployeeORM.rule),
                    selectinload(EmployeeORM.authentication)
                )
                .filter(
                    EmployeeORM.employee_active == "1",
                    EmployeeORM.employee_login == username
                )
                .first()
            )
                
            if row is None:
                raise UserNotFoundException(
                    f"Prescription with username: {username} not found"
                )
            
            return _to_user(row)
            