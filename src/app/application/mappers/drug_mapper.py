from app.domain.entities.drug import Drug, DrugImage, DrugImageList, DrugList, DrugImageUpload, ImageVariantList, DrugImageListUpload
from app.application.dto.drug_dto import DrugDTO, DrugImageDTO, DrugImageListDTO, DrugListDTO, DrugListItemDTO, DrugNameDTO, DrugCategoryDTO, DrugFlagsDTO, DrugInstructionDTO, DrugImageInputDTO

def _to_drug(dto: DrugDTO) -> Drug:
    return Drug(
        b_item_id = dto.b_item_id,
        item_number = dto.item_number,
        item_common_name = dto.item_common_name,
        item_trade_name = dto.item_trade_name,
        item_nick_name = dto.item_nick_name,   
        item_active = dto.item_active,
        b_item_subgroup = dto.b_item_subgroup,
        b_item_billing_subgroup = dto.b_item_billing_subgroup,   
        b_item_16_group = dto.b_item_16_group,
        images = dto.images,
        instructions = dto.instructions
    )

def _to_image_dto(image: DrugImage) -> DrugImageDTO:
    return DrugImageDTO(
        id = image.id,
        image_url = image.image_url,
        view_type = image.view_type,
        position = image.position,
        lighting = image.lighting,
        created_at = image.created_at
    )

def _to_dto(drug: Drug) -> DrugDTO:
    return DrugDTO(
        id = drug.b_item_id,
        code = drug.item_number,
        names = DrugNameDTO(
            generic = drug.item_common_name,
            trade = drug.item_trade_name,
            thai = drug.item_nick_name
        ),
        categories = DrugCategoryDTO(
            therapeutic = drug.b_item_subgroup,
            pharmacological = drug.b_item_billing_subgroup,
            standard = drug.b_item_16_group
        ),
        images = [
            _to_image_dto(image)
            for image in drug.images
        ] if drug.images else [],
        instructions = DrugInstructionDTO(
            caution = drug.instructions[0].item_drug_caution if drug.instructions else "",
            description = drug.instructions[0].item_drug_description if drug.instructions else "",
            special_prescription = drug.instructions[0].item_drug_special_prescription_text if drug.instructions else "",
            instruction = drug.instructions[0].instruction_text if drug.instructions else "",
        )
    )

def _to_dto_list(drugs: DrugList) -> DrugListDTO:
    return DrugListDTO(
        drugs = [
            DrugListItemDTO(
                drug_id = drug.drug_id,
                drug_code = drug.drug_code,
                drug_common_name = drug.drug_common_name,
                flags = DrugFlagsDTO(
                    is_high_alert = drug.flags.is_high_alert,
                    has_images = drug.flags.has_images
                ),
            )
            for drug in drugs.drugs
        ],
        total = drugs.total,
        page = drugs.page,
        size = drugs.size
    )

def _to_drug_image_upload(image: DrugImageInputDTO, variant_id: int) -> DrugImageUpload:
    return DrugImageUpload(
        content = image.content,
        content_type = image.content_type,
        variant_id = variant_id,
        view_type = image.view_type,
        position = image.position,
        lighting = image.lighting
    )

def _to_drug_image_list_upload(id: str, images: list[DrugImageUpload]) -> DrugImageListUpload:
    return DrugImageListUpload(
        b_item_id = id,
        images = images
    )

def _to_drug_image_list_dto(images: DrugImageList) -> DrugImageListDTO:
    return DrugImageListDTO(
        images = [
            DrugImage(
                id = image.id,
                image_url = image.image_url,
                view_type = image.view_type,
                position = image.position,
                lighting = image.lighting,
                created_at = image.created_at
            )
            for image in images.images
        ]
    )