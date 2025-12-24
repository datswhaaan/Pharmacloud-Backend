from sqlalchemy import Column, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DrugORM(Base):
    __tablename__ = "drugs"
    drug_code = Column(String, primary_key=True, index=True)
    width_mm = Column(Float, index=True)
    length_mm = Column(Float, index=True)
    height_mm = Column(Float, index=True)
    weight_mg = Column(Float, index=True)
    image_top_path = Column(String, index=True)
    image_side_path = Column(String, index=True)
    image_front_path = Column(String, index=True)
    image_top_path2 = Column(String, index=True)
    image_side_path2 = Column(String, index=True)
    image_front_path2 = Column(String, index=True)