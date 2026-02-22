from app.domain.entities.drug import Drug, DrugList
from app.application.dto.drug_dto import DrugDTO, DrugListDTO

def _to_drug(dto: DrugDTO) -> Drug:
    return Drug(
        b_item_id = dto.b_item_id,
        item_number = dto.item_number,
        item_common_name = dto.item_common_name,
        item_trade_name = dto.item_trade_name,
        item_nick_name = dto.item_nick_name,   
        item_active = dto.item_active,
        b_item_subgroup_id = dto.b_item_subgroup_id,
        b_item_billing_subgroup_id = dto.b_item_billing_subgroup_id,   
        item_printable = dto.item_printable,
        item_secret = dto.item_secret,
        b_item_16_group_id = dto.b_item_16_group_id,
        f_item_lab_type_id = dto.f_item_lab_type_id,
        b_specimen_id = dto.b_specimen_id
    )

def _to_dto(drug: Drug) -> DrugDTO:
    return DrugDTO(
        b_item_id = drug.b_item_id,
        item_number = drug.item_number,
        item_common_name = drug.item_common_name,
        item_trade_name = drug.item_trade_name,
        item_nick_name = drug.item_nick_name,   
        item_active = drug.item_active,
        b_item_subgroup_id = drug.b_item_subgroup_id,
        b_item_billing_subgroup_id = drug.b_item_billing_subgroup_id,   
        item_printable = drug.item_printable,
        item_secret = drug.item_secret,
        b_item_16_group_id = drug.b_item_16_group_id,
        f_item_lab_type_id = drug.f_item_lab_type_id,
        b_specimen_id = drug.b_specimen_id
    )

def _to_dto_list(drugs: DrugList) -> DrugListDTO:
    return DrugListDTO(
        drugs = [
            _to_dto(drug)
            for drug in drugs.drugs
        ]
    )