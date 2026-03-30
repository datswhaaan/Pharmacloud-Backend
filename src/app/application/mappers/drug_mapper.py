from app.domain.entities.drug import Drug, DrugImage, DrugList
from app.application.dto.drug_dto import DrugDTO, DrugImageDTO, DrugListDTO, DrugListItemDTO

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
        image_url = image.image_url,
        view_type = image.view_type,
        position = image.position,
        lighting = image.lighting
    )

def _to_dto(drug: Drug) -> DrugDTO:
    return DrugDTO(
        b_item_id = drug.b_item_id,
        item_number = drug.item_number,
        item_common_name = drug.item_common_name,
        item_trade_name = drug.item_trade_name,
        item_nick_name = drug.item_nick_name,   
        item_active = drug.item_active,
        b_item_subgroup = drug.b_item_subgroup,
        b_item_billing_subgroup = drug.b_item_billing_subgroup,
        b_item_16_group = drug.b_item_16_group,
        images = list[DrugImageDTO](
            _to_image_dto(image) for image in drug.images
        ) if drug.images else None,
        instructions = drug.instructions
    )

def _to_dto_list(drugs: DrugList) -> DrugListDTO:
    return DrugListDTO(
        drugs = [
            DrugListItemDTO(
                item_number = drug.item_number,
                item_common_name = drug.item_common_name,
                high_alert = drug.high_alert
            )
            for drug in drugs.drugs
        ],
        total = drugs.total,
        page = drugs.page,
        size = drugs.size
    )