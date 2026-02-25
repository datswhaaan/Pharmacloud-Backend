from app.domain.entities.drug import DrugImage, DrugImageList
from app.presentation.schemas.drug import DrugImageListDTO, DrugSchema
from app.application.dto.drug_dto import DrugDTO, DrugImageListDTO

def _schema_to_drug_dto(input: DrugSchema) -> DrugDTO:
    return DrugDTO(**input.model_dump())

def _to_drug_image_list_dto(id: str, input: DrugImageListDTO) -> DrugImageList:

    domain_images = DrugImageList(
        b_item_id=id,
        images=[
            DrugImage(
                image_url=i.image_url,
                view_type=i.view_type,
                position=i.position,
                lighting=i.lighting
            )
            for i in input.images
        ]
    )
    
    return domain_images