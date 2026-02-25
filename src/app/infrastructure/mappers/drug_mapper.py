from app.infrastructure.models.drug import DrugORM, DrugImageORM, DrugInstructionORM, ImageVariantORM, InstructionORM
from app.domain.entities.drug import Drug, DrugList, DrugImage, DrugInstruction, ImageVariant, ImageVariant, ImageVariantList, DrugListItem

def _to_drug_image(orm: DrugImageORM) -> DrugImage:
    return DrugImage(
        image_url = orm.image_url,
        variant_id = orm.variant_id
    )

def _to_drug_image_orm(id: str, drug_image: DrugImage) -> DrugImageORM:
    return DrugImageORM(
        b_item_id = id,
        image_url = drug_image.image_url,
        variant_id = drug_image.variant_id
    )

def _to_drug_instruction(orm: DrugInstructionORM) -> DrugInstruction:
    return DrugInstruction(
        b_item_drug_id = orm.b_item_drug_id,
        b_item_id = orm.b_item_id,
        item_drug_caution = orm.item_drug_caution,
        b_item_drug_instruction_id = orm.b_item_drug_instruction_id,
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
        b_item_subgroup_id = orm.b_item_subgroup_id,
        b_item_billing_subgroup_id = orm.b_item_billing_subgroup_id,   
        b_item_16_group_id = orm.b_item_16_group_id,
        images = [
            _to_drug_image(image) for image in orm.images],
        instructions = [
            _to_drug_instruction(instruction) for instruction in orm.instructions]
    )

def _to_drug_list(ormlist: list[DrugORM]) ->  DrugList:
    return DrugList(
        drugs = [
            DrugListItem(
                item_number = orm.item_number,
                item_common_name = orm.item_common_name,
                high_alert = orm.high_alert
            )
            for orm in ormlist
        ]
    )

def _to_drug_orm(drug: Drug) -> DrugORM:
    return DrugORM(
            b_item_id = drug.b_item_id,
            item_number = drug.item_number,
            item_common_name = drug.item_common_name,
            item_trade_name = drug.item_trade_name,
            item_nick_name = drug.item_nick_name,   
            item_active = drug.item_active,
            b_item_subgroup_id = drug.b_item_subgroup_id,
            b_item_billing_subgroup_id = drug.b_item_billing_subgroup_id,   
            b_item_16_group_id = drug.b_item_16_group_id,
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