from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class VisitTypeORM(Base):
    __tablename__ = "f_visit_type"
    f_visit_type_id = Column(String, primary_key=True, index=True)
    visit_type_description = Column(String)

    prescriptions = relationship("PrescriptionORM", back_populates="visit_type")

class SexORM(Base):
    __tablename__ = "f_sex"
    f_sex_id = Column(String, primary_key=True, index=True)
    sex_description = Column(String)

    patient_prefix = relationship("PatientPrefixORM", back_populates="sex")

class PatientPrefixORM(Base):
    __tablename__ = "f_patient_prefix"
    f_patient_prefix_id = Column(String, primary_key=True, index=True)
    patient_prefix_description = Column(String)
    f_sex_id = Column(String, ForeignKey("f_sex.f_sex_id"))

    sex = relationship("SexORM", back_populates="patient_prefix")
    patient_prefix = relationship("PatientORM", back_populates="prefix")

class PatientORM(Base):
    __tablename__ = "t_patient"
    t_patient_id = Column(String, primary_key=True, index=True)
    patient_hn = Column(String, index=True)
    f_patient_prefix_id = Column(String, ForeignKey("f_patient_prefix.f_patient_prefix_id"))
    patient_firstname = Column(String)
    patient_lastname = Column(String)

    prefix = relationship("PatientPrefixORM", back_populates="patient_prefix")
    prescriptions = relationship("PrescriptionORM", back_populates="patient")
    risk_factors = relationship("PatientRiskFactorORM", back_populates="patient")

class EmployeeORM(Base):
    __tablename__ = "b_employee"
    b_employee_id = Column(String, primary_key=True, index=True)
    employee_firstname = Column(String)
    employee_lastname = Column(String)

    prescriptions = relationship("PrescriptionORM", back_populates="employee")

class PrescriptionORM(Base):
    __tablename__ = "t_visit"
    t_visit_id = Column(String, primary_key=True, index=True)
    visit_hn = Column(String, index=True)
    visit_vn = Column(String, index=True)
    f_visit_type_id = Column(String, ForeignKey("f_visit_type.f_visit_type_id"), index=True)
    visit_begin_visit_time = Column(String, index=True)
    visit_diagnosis_notice = Column(String)
    visit_patient_type = Column(String)
    visit_queue = Column(String)
    visit_dx = Column(String)
    t_patient_id = Column(String, ForeignKey("t_patient.t_patient_id", ondelete="CASCADE"), index=True)
    visit_staff_doctor_discharge = Column(String, ForeignKey("b_employee.b_employee_id", ondelete="CASCADE"), index=True)
    visit_deny_allergy = Column(String)
    visit_patient_age = Column(String)

    visit_type = relationship("VisitTypeORM", back_populates="prescriptions")
    patient = relationship("PatientORM", back_populates="prescriptions")
    employee = relationship("EmployeeORM", back_populates="prescriptions")
    orders = relationship("OrderORM", back_populates="visit")

class PatientRiskFactorORM(Base):
    __tablename__ = "t_patient_risk_factor"
    t_patient_risk_factor_id = Column(String, primary_key=True, index=True)
    t_patient_id = Column(String, ForeignKey("t_patient.t_patient_id", ondelete="CASCADE"), index=True)
    patient_risk_factor_description = Column(String)
    patient_risk_factor_topic = Column(String)

    patient = relationship("PatientORM", back_populates="risk_factors")

class OrderORM(Base):
    __tablename__ = "t_order"
    t_order_id = Column(String, primary_key=True, index=True)
    t_visit_id = Column(String, ForeignKey("t_visit.t_visit_id", ondelete="CASCADE"), index=True)
    b_item_id = Column(String, ForeignKey("b_item.b_item_id", ondelete="CASCADE"), index=True)
    order_secret = Column(String)
    order_common_name = Column(String)
    order_qty = Column(Float)

    visit = relationship("PrescriptionORM", back_populates="orders")
    item = relationship("ItemORM", back_populates="orders")
    order_drugs = relationship("OrderDrugORM", back_populates="order")

class OrderDrugORM(Base):
    __tablename__ = "t_order_drug"
    t_order_drug_id = Column(String, primary_key=True, index=True)
    t_order_id = Column(String, ForeignKey("t_order.t_order_id", ondelete="CASCADE"), index=True)
    b_item_id = Column(String, ForeignKey("b_item.b_item_id", ondelete="CASCADE"), index=True)
    b_item_drug_uom_id_purch = Column(String, ForeignKey("b_item_drug_uom.b_item_drug_uom_id", ondelete="CASCADE"), index=True)
    order_drug_dose = Column(Float)

    order = relationship("OrderORM", back_populates="order_drugs")
    item = relationship("ItemORM", back_populates="order_drugs")
    item_drug_uom = relationship("ItemDrugUOMORM", back_populates="order_drugs")

class ItemORM(Base):
    __tablename__ = "b_item"
    b_item_id = Column(String, primary_key=True, index=True)
    item_common_name = Column(String)

    orders = relationship("OrderORM", back_populates="item")
    order_drugs = relationship("OrderDrugORM", back_populates="item")

class ItemDrugUOMORM(Base):
    __tablename__ = "b_item_drug_uom"
    b_item_drug_uom_id = Column(String, primary_key=True, index=True)
    item_drug_uom_description = Column(String)

    order_drugs = relationship("OrderDrugORM", back_populates="item_drug_uom")