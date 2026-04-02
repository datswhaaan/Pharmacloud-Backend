from app.infrastructure.models.drug import DrugORM, DrugImageORM, DrugInstructionORM, ImageVariantORM, InstructionORM
from app.domain.entities.drug import Drug, DrugList, DrugImage, DrugInstruction, ImageVariant, ImageVariant, ImageVariantList, DrugListItem, DrugImageUpload

def _to_drug_image(orm: DrugImageORM) -> DrugImage:
    return DrugImage(
        id = orm.drug_image_id,
        image_url = orm.image_url,
        view_type = orm.variant.view_type,
        position = orm.variant.position,
        lighting = orm.variant.lighting,
        created_at = orm.created_at
    )

def _to_drug_image_orm(drug_id: str, drug_image: DrugImageUpload, drug_image_url: str) -> DrugImageORM:
    return DrugImageORM(
        b_item_id = drug_id,
        image_url = drug_image_url,
        variant_id = drug_image.variant_id
    )

def _to_drug_instruction(orm: DrugInstructionORM) -> DrugInstruction:
    return DrugInstruction(
        item_drug_caution = orm.item_drug_caution,
        item_drug_description = orm.item_drug_description,
        item_drug_special_prescription_text = orm.item_drug_special_prescription_text,
        instruction_text = orm.instruction.item_drug_instruction_description,
        high_alert = orm.height_alert == "Y"
    )

def _to_drug(orm: DrugORM) -> Drug:
    return Drug(
        b_item_id = orm.b_item_id,
        item_number = orm.item_number,
        item_common_name = orm.item_common_name,
        item_trade_name = orm.item_trade_name,
        item_nick_name = orm.item_nick_name,   
        item_active = orm.item_active,
        b_item_subgroup = orm.subgroup.item_subgroup_number + " " + orm.subgroup.item_subgroup_description if orm.subgroup else None,
        b_item_billing_subgroup = orm.billing_subgroup.item_billing_subgroup_number + " " + orm.billing_subgroup.item_billing_subgroup_description if orm.billing_subgroup else None,
        b_item_16_group = orm.group_16.item_16_group_number + " " + orm.group_16.item_16_group_description if orm.group_16 else None,
        images = [
            _to_drug_image(image) for image in orm.images],
        instructions = [
            _to_drug_instruction(instruction) for instruction in orm.instructions]
    )

def _to_drug_list(ormlist: list[DrugORM], total: int, page: int, size: int) ->  DrugList:
    return DrugList(
        drugs = [
            DrugListItem(
                drug_id = orm.b_item_id,
                drug_code = orm.item_number,
                drug_common_name = orm.item_common_name,
                high_alert = orm.high_alert
            )
            for orm in ormlist
        ],
        total = total,
        page = page,
        size = size
    )

def _to_drug_orm(drug: Drug) -> DrugORM:
    return DrugORM(
            b_item_id = drug.b_item_id,
            item_number = drug.item_number,
            item_common_name = drug.item_common_name,
            item_trade_name = drug.item_trade_name,
            item_nick_name = drug.item_nick_name,   
            item_active = drug.item_active,
            b_item_subgroup = drug.b_item_subgroup,
            b_item_billing_subgroup = drug.b_item_billing_subgroup,   
            b_item_16_group = drug.b_item_16_group,
        )

def to_image_variant_list(ormlist: list[ImageVariantORM]) -> ImageVariantList:
    return ImageVariantList(
        variants=[
            ImageVariant(
                variant_id=orm.variant_id,
                view_type=orm.view_type,
                position=orm.position,
                lighting=orm.lighting,
                description=orm.description
        )
        for orm in ormlist
    ])