from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DrugORM(Base):
    __tablename__ = "b_item"
    b_item_id = Column(String, primary_key=True, index=True)
    item_number = Column(String, index=True)
    item_common_name = Column(String, index=True)
    item_trade_name = Column(String, index=True)
    item_nick_name = Column(String, index=True)
    item_active = Column(String, index=True)
    b_item_subgroup_id = Column(String, index=True)
    b_item_billing_subgroup_id = Column(String, index=True)
    item_printable = Column(String)
    item_secret = Column(String)
    b_item_16_group_id = Column(String, index=True)
    r_rp1253_adpcode_id = Column(String)
    item_unit_packing_qty = Column(String)
    f_item_lab_type_id = Column(String)
    r_rp1253_charitem_id = Column(String)
    item_specified = Column(String)
    item_general_number = Column(String)
    doctor_warning_icd10_idx = Column(String)
    b_specimen_id = Column(String)