from app.infrastructure.models.drug_metadata import DrugMetadataORM
from app.domain.entities.drug_metadata import DrugMetadata, DrugMetadataList

def _to_drug(orm: DrugMetadataORM) -> DrugMetadata:
    return DrugMetadata(
        drug_code = orm.drug_code,
        width_mm = orm.width_mm,
        length_mm = orm.length_mm,
        height_mm = orm.height_mm,
        weight_mg = orm.weight_mg,   
        image_top_path = orm.image_top_path,
        image_side_path = orm.image_side_path,
        image_front_path = orm.image_front_path,   
        image_top_path2 = orm.image_top_path2,
        image_side_path2 = orm.image_side_path2,
        image_front_path2 = orm.image_front_path2
    )

def _to_drug_list(ormlist: list[DrugMetadataORM]) -> DrugMetadataList:
    return DrugMetadataList(
        drugs = [
            _to_drug(item)
            for item in ormlist
        ]
    )

def _to_drug_orm(drug: DrugMetadata) -> DrugMetadataORM:
    return DrugMetadataORM(
            drug_code = drug.drug_code,
            width_mm = drug.width_mm,
            length_mm = drug.length_mm,
            height_mm = drug.height_mm,
            weight_mg = drug.weight_mg,   
            image_top_path = drug.image_top_path,
            image_side_path = drug.image_side_path,
            image_front_path = drug.image_front_path,   
            image_top_path2 = drug.image_top_path2,
            image_side_path2 = drug.image_side_path2,
            image_front_path2 = drug.image_front_path2
        )