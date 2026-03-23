from app.infrastructure.models.user import EmployeeORM
from app.domain.entities.user import User

def _to_user(emp: EmployeeORM) -> User:
    return User(
        user_id=emp.b_employee_id,
        username=emp.employee_login,
        hashed_password=emp.employee_password,
        role=emp.level.employee_level_description,
        firstname=emp.employee_firstname,
        lastname=emp.employee_lastname,
        authentication=emp.authentication.employee_authentication_description
    )