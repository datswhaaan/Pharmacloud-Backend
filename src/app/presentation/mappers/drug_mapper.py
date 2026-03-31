from app.domain.entities.drug import DrugImage, DrugImageList
from app.presentation.schemas.drug import DrugImageListDTO
from app.application.dto.drug_dto import DrugDTO, DrugImageListDTO, DrugListDTO, DrugImageDTO
from app.presentation.schemas.drug_response import DrugImageResponse, DrugResponse, DrugListResponse, DrugListItemResponse

def _to_drug_image_response(image: DrugImageDTO) -> DrugImageResponse:
    return DrugImageResponse(
        image_url = image.image_url,
        view_type = image.view_type,
        position = image.position,
        lighting = image.lighting
    )

def _to_drug_response(dto: DrugDTO) -> DrugResponse:
    return DrugResponse(
        b_item_id = dto.b_item_id,
        item_number = dto.item_number,
        item_common_name = dto.item_common_name,
        item_trade_name = dto.item_trade_name,
        item_nick_name = dto.item_nick_name,   
        item_active = dto.item_active,
        b_item_subgroup = dto.b_item_subgroup,
        b_item_billing_subgroup = dto.b_item_billing_subgroup,
        b_item_16_group = dto.b_item_16_group,
        images=[
            _to_drug_image_response(img)
            for img in (dto.images or [])
        ],
        instructions=dto.instructions or []
    )

def _to_drug_list_response(dto: DrugListDTO) -> DrugListResponse:
    return DrugListResponse(
        drugs = [
            DrugListItemResponse(
                drug_id = drug.drug_id,
                drug_code = drug.drug_code,
                drug_common_name = drug.drug_common_name,
                high_alert = drug.high_alert
            )
            for drug in dto.drugs
        ],
        total = dto.total,
        page = dto.page,
        size = dto.size
    )

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