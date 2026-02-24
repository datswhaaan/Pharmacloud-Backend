import uuid

from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ImageVariantORM(Base):
    __tablename__ = "image_variants"
    variant_id = Column(Integer, primary_key=True, index=True)
    variant_name = Column(String)
    description = Column(String)
    images = relationship("DrugImageORM", back_populates="variant")

class DrugImageORM(Base):
    __tablename__ = "drug_images"
    drug_image_id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    b_item_id = Column(String, ForeignKey("b_item.b_item_id", ondelete="CASCADE"),index=True)
    variant_id = Column(Integer, ForeignKey("image_variants.variant_id"), index=True)
    image_url = Column(String)
    description = Column(String)
    drug = relationship("DrugORM", back_populates="images")
    variant = relationship("ImageVariantORM", back_populates="images")

class InstructionORM(Base):
    __tablename__ = "b_item_drug_instruction"
    b_item_drug_instruction_id = Column(String, primary_key=True, index=True)
    item_drug_instruction_description = Column(String)
    item_drug_instruction_active = Column(String)
    drug_instructions = relationship("DrugInstructionORM", back_populates="instruction")

class DrugInstructionORM(Base):
    __tablename__ = "b_item_drug"
    b_item_drug_id = Column(String, primary_key=True, index=True)
    b_item_id = Column(String, ForeignKey("b_item.b_item_id", ondelete="CASCADE"), index=True)
    item_drug_caution = Column(String)
    b_item_drug_instruction_id = Column(String, ForeignKey("b_item_drug_instruction.b_item_drug_instruction_id"), index=True)
    item_drug_description = Column(String)
    item_drug_special_prescription_text = Column(String)
    height_alert = Column(String)
    drug = relationship("DrugORM", back_populates="instructions")
    instruction = relationship("InstructionORM", back_populates="drug_instructions")

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
    b_item_16_group_id = Column(String, index=True)
    images = relationship("DrugImageORM", back_populates="drug")
    instructions = relationship("DrugInstructionORM", back_populates="drug")