from app.domain.entities.drug import DrugImage, DrugImageList
from app.presentation.schemas.drug import DrugImageListDTO
from app.application.dto.drug_dto import DrugDTO, DrugImageListDTO, DrugListDTO, DrugImageDTO
from app.presentation.schemas.drug_response import DrugImageResponse, DrugResponse, DrugListResponse, DrugListItemResponse, DrugNameResponse, DrugCategoryResponse, DrugFlagsResponse, DrugInstructionResponse

def _to_drug_image_response(image: DrugImageDTO) -> DrugImageResponse:
    return DrugImageResponse(
        id = image.id,
        url = image.image_url,
        view_type = image.view_type,
        position = image.position,
        lighting = image.lighting,
        created_at = image.created_at
    )

def _to_drug_response(dto: DrugDTO) -> DrugResponse:
    return DrugResponse(
        id = dto.id,
        code = dto.code,
        names = DrugNameResponse(
            generic = dto.names.generic,
            trade = dto.names.trade,
            thai = dto.names.thai
        ),
        categories = DrugCategoryResponse(
            therapeutic = dto.categories.therapeutic,
            pharmacological = dto.categories.pharmacological,
            standard = dto.categories.standard
        ),
        flags = DrugFlagsResponse(
            is_high_alert = dto.flags.is_high_alert,
            is_new_drug = dto.flags.is_new_drug,
            has_images = dto.flags.has_images
        ),
        images=[
            _to_drug_image_response(img)
            for img in (dto.images or [])
        ],
        instructions=DrugInstructionResponse(
            caution = dto.instructions.caution,
            description = dto.instructions.description,
            special_prescription = dto.instructions.special_prescription,
            instruction = dto.instructions.instruction
        )
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