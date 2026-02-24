from app.infrastructure.models.drug import DrugORM, DrugImageORM, DrugInstructionORM, InstructionORM
from app.domain.entities.drug import Drug, DrugList, DrugImage, DrugInstruction

def _to_drug_image(orm: DrugImageORM) -> DrugImage:
    return DrugImage(
        b_item_image_id = orm.b_item_image_id,
        b_item_id = orm.b_item_id,
        item_image_url = orm.item_image_url,
        f_image_variant_id = orm.f_image_variant_id
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
            _to_drug(drug)
            for drug in ormlist
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