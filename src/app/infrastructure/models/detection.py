from sqlalchemy import Column, ForeignKey, String, Float, DateTime, Integer, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DetectionStatusORM(Base):
    __tablename__ = "detection_status"
    detection_status_id = Column(Integer, primary_key=True, index=True)
    detection_status_description = Column(String)

    detection = relationship("DetectionORM", back_populates="detection_status")

class DetectionORM(Base):
    __tablename__ = "detection"
    detection_id = Column(String, primary_key=True, index=True)
    t_order_id = Column(String, ForeignKey("t_order.t_order_id", ondelete="CASCADE"), index=True)
    detected_at = Column(DateTime)
    image_url = Column(String)
    verified_by = Column(String, ForeignKey("b_employee.b_employee_id"))
    verified_at = Column(DateTime)
    status_id = Column(Integer, ForeignKey("detection_status.detection_status_id"))

    orders = relationship("OrderORM", back_populates="detection")
    detection_item = relationship("DetectionItemORM", back_populates="detection")
    employee = relationship("EmployeeORM", back_populates="detection")
    detection_status = relationship("DetectionStatusORM", back_populates="detection")

class DetectionItemORM(Base):
    __tablename__ = "detection_item"
    detection_item_id = Column(String, primary_key= True, index=True)
    detection_id = Column(String, ForeignKey("detection.detection_id"))
    t_order_drug_id = Column(String, ForeignKey("t_order_drug.t_order_drug_id"))
    b_item_id = Column(String, ForeignKey("b_item.b_item_id"))
    confidence = Column(Float)
    quantity = Column(Integer)
    is_manually_edited = Column(Boolean)

    detection = relationship("DetectionORM", back_populates="detection_item")
    order_drugs = relationship("OrderDrugORM", back_populates="detection_item")
    item = relationship("ItemORM", back_populates="detection_item")


class OrderORM(Base):
    __tablename__ = "t_order"
    t_order_id = Column(String, primary_key=True, index=True)
    b_item_id = Column(String, ForeignKey("b_item.b_item_id", ondelete="CASCADE"), index=True)
    order_common_name = Column(String)
    order_qty = Column(Float)

    item = relationship("ItemORM", back_populates="orders")
    order_drugs = relationship("OrderDrugORM", back_populates="orders")
    detection = relationship("DetectionORM", back_populates="orders")


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