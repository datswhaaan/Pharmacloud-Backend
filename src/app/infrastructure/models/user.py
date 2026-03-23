from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class EmployeeLevelORM(Base):
    __tablename__ = "f_employee_level"
    f_employee_level_id = Column(String, primary_key=True, index=True)
    employee_level_description = Column(String)

    employee = relationship("EmployeeORM", back_populates="level")

class EmployeeRuleORM(Base):
    __tablename__ = "f_employee_rule"
    f_employee_rule_id = Column(String, primary_key=True, index=True)
    employee_rule_description = Column(String)

    employee = relationship("EmployeeORM", back_populates="rule")

class EmployeeAuthenticationORM(Base):
    __tablename__ = "f_employee_authentication"
    f_employee_authentication_id = Column(String, primary_key=True, index=True)
    employee_authentication_description = Column(String)

    employee = relationship("EmployeeORM", back_populates="authentication")

class EmployeeORM(Base):
    __tablename__ = "b_employee"
    b_employee_id = Column(String, primary_key=True, index=True)
    employee_login = Column(String, index=True)
    employee_password = Column(String)
    employee_firstname = Column(String, index=True)
    employee_lastname = Column(String, index=True)
    employee_last_login = Column(String)
    employee_last_logout = Column(String)
    employee_active = Column(String)
    f_employee_level_id = Column(String, ForeignKey("f_employee_level.f_employee_level_id"))
    f_employee_rule_id = Column(String, ForeignKey("f_employee_rule.f_employee_rule_id"))
    f_employee_authentication_id = Column(String, ForeignKey("f_employee_authentication.f_employee_authentication_id"),index=True )

    level = relationship("EmployeeLevelORM", back_populates="employee")
    rule = relationship("EmployeeRuleORM", back_populates="employee")
    authentication = relationship("EmployeeAuthenticationORM", back_populates="employee")