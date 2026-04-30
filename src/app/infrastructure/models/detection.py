from sqlalchemy import Column, ForeignKey, String, Float, DateTime, Integer, Boolean, Enum, text, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DetectionORM(Base):
    __tablename__ = "detection"
    detection_id = Column(String, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    t_order_id = Column(String, ForeignKey("t_order.t_order_id", ondelete="CASCADE"), index=True)
    detected_at = Column(DateTime, server_default=func.now())
    image_url = Column(String)
    verified_by = Column(String, ForeignKey("b_employee.b_employee_id"))
    verified_at = Column(DateTime)
    status = Column(Enum("UNVERIFIED", "APPROVED", "REJECTED", "MODIFIED", "CANCELLED", name="detection_status_enum"))
    created_at = Column(DateTime)

    orders = relationship("OrderORM", back_populates="detection")
    detection_item = relationship("DetectionItemORM", back_populates="detection")
    employee = relationship("EmployeeORM", back_populates="detection")

class DetectionItemORM(Base):
    __tablename__ = "detection_item"
    detection_item_id = Column(String, primary_key= True, index=True, server_default=text("gen_random_uuid()"))
    detection_id = Column(String, ForeignKey("detection.detection_id"))
    t_order_drug_id = Column(String, ForeignKey("t_order_drug.t_order_drug_id"))
    b_item_id = Column(String, ForeignKey("b_item.b_item_id"))
    confidence = Column(Float)
    quantity = Column(Integer)
    is_manually_edited = Column(Boolean, server_default=text("false"))
    match_type = Column(Enum("MATCHED", "EXTRA", name="match_type_enum"))
    error_type = Column(Enum("WRONG_DRUG_NAME", "WRONG_STRENGTH", "WRONG_QUANTITY", "WRONG_FORM", name="error_type_enum"))

    detection = relationship("DetectionORM", back_populates="detection_item")
    order_drugs = relationship("OrderDrugORM", back_populates="detection_item")
    item = relationship("ItemORM", back_populates="detection_item")


class OrderORM(Base):
    __tablename__ = "t_order"
    t_order_id = Column(String, primary_key=True, index=True)
    t_visit_id = Column(String, ForeignKey("t_visit.t_visit_id", ondelete="CASCADE"), index=True)
    b_item_id = Column(String, ForeignKey("b_item.b_item_id", ondelete="CASCADE"), index=True)
    order_common_name = Column(String)
    order_qty = Column(Float)
    f_order_status_id = Column(String, ForeignKey("f_order_status.f_order_status_id", ondelete="CASCADE"), index=True)

    item = relationship("ItemORM", back_populates="orders")
    order_drugs = relationship("OrderDrugORM", back_populates="orders")
    detection = relationship("DetectionORM", back_populates="orders")
    order_status = relationship("OrderStatusORM", back_populates="orders")
    visit = relationship("VisitORM", back_populates="orders")

class OrderDrugORM(Base):
    __tablename__ = "t_order_drug"
    t_order_drug_id = Column(String, primary_key=True, index=True)
    t_order_id = Column(String, ForeignKey("t_order.t_order_id", ondelete="CASCADE"), index=True)
    b_item_id = Column(String, ForeignKey("b_item.b_item_id", ondelete="CASCADE"), index=True)
    b_item_drug_uom_id_purch = Column(String, ForeignKey("b_item_drug_uom.b_item_drug_uom_id", ondelete="CASCADE"), index=True)
    order_drug_dose = Column(Float)

    orders = relationship("OrderORM", back_populates="order_drugs")
    item = relationship("ItemORM", back_populates="order_drugs")
    item_drug_uom = relationship("ItemDrugUOMORM", back_populates="order_drugs")
    detection_item = relationship("DetectionItemORM", back_populates="order_drugs")

class EmployeeORM(Base):
    __tablename__ = "b_employee"
    b_employee_id = Column(String, primary_key=True, index=True)
    employee_firstname = Column(String)
    employee_lastname = Column(String)

    detection = relationship("DetectionORM", back_populates="employee")

class ItemORM(Base):
    __tablename__ = "b_item"
    b_item_id = Column(String, primary_key=True, index=True)
    item_common_name = Column(String)

    orders = relationship("OrderORM", back_populates="item")
    order_drugs = relationship("OrderDrugORM", back_populates="item")
    detection_item = relationship("DetectionItemORM", back_populates="item")
    item_drug = relationship("ItemDrugORM", back_populates="item")

class ItemDrugORM(Base):
    __tablename__ = "b_item_drug"
    b_item_drug_id = Column(String, primary_key=True, index=True)
    b_item_id = Column(String, ForeignKey("b_item.b_item_id", ondelete="CASCADE"), index=True)
    item_drug_purch_uom = Column(String, ForeignKey("b_item_drug_uom.b_item_drug_uom_id"))

    item = relationship("ItemORM", back_populates="item_drug")
    item_drug_uom = relationship("ItemDrugUOMORM", back_populates="item_drug")

class ItemDrugUOMORM(Base):
    __tablename__ = "b_item_drug_uom"
    b_item_drug_uom_id = Column(String, primary_key=True, index=True)
    item_drug_uom_description = Column(String)

    order_drugs = relationship("OrderDrugORM", back_populates="item_drug_uom")
    item_drug = relationship("ItemDrugORM", back_populates="item_drug_uom")

class PatientPrefixORM(Base):
    __tablename__ = "f_patient_prefix"
    f_patient_prefix_id = Column(String, primary_key=True, index=True)
    patient_prefix_description = Column(String)

    patient_prefix = relationship("PatientORM", back_populates="prefix")

class PatientORM(Base):
    __tablename__ = "t_patient"
    t_patient_id = Column(String, primary_key=True, index=True)
    patient_hn = Column(String, index=True)
    f_patient_prefix_id = Column(String, ForeignKey("f_patient_prefix.f_patient_prefix_id"))
    patient_firstname = Column(String)
    patient_lastname = Column(String)

    prefix = relationship("PatientPrefixORM", back_populates="patient_prefix")
    visit = relationship("VisitORM", back_populates="patient")

class VisitORM(Base):
    __tablename__ = "t_visit"
    t_visit_id = Column(String, primary_key=True, index=True)
    visit_hn = Column(String, index=True)
    visit_vn = Column(String, index=True)
    visit_begin_visit_time = Column(String, index=True)
    t_patient_id = Column(String, ForeignKey("t_patient.t_patient_id", ondelete="CASCADE"), index=True)

    patient = relationship("PatientORM", back_populates="visit")
    orders = relationship("OrderORM", back_populates="visit")

class OrderStatusORM(Base):
    __tablename__ = "f_order_status"
    f_order_status_id = Column(String, primary_key=True, index=True)
    order_status_description = Column(String)

    orders = relationship("OrderORM", back_populates="order_status")