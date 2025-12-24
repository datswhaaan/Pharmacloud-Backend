from app.domain.entities.drug import Drug, DrugList
from app.application.dto.drug_dto import DrugDTO, DrugListDTO

def _to_drug(dto: DrugDTO) -> Drug:
    return Drug(
        drug_code = dto.drug_code,
        width_mm = dto.width_mm,
        length_mm = dto.length_mm,
        height_mm = dto.height_mm,
        weight_mg = dto.weight_mg,   
        image_top_path = dto.image_top_path,
        image_side_path = dto.image_side_path,
        image_front_path = dto.image_front_path,   
        image_top_path2 = dto.image_top_path2,
        image_side_path2 = dto.image_side_path2,
        image_front_path2 = dto.image_front_path2
    )

def _to_dto(drug: Drug) -> DrugDTO:
    return DrugDTO(
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

def _to_dto_list(drugs: DrugList) -> DrugListDTO:
    return DrugListDTO(
        drugs = [
            _to_dto(drug)
            for drug in drugs.drugs
        ]
    )