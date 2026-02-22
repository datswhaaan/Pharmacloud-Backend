from app.infrastructure.models.drug import DrugORM
from app.domain.entities.drug import Drug, DrugList

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
        item_printable = orm.item_printable,
        item_secret = orm.item_secret,
        b_item_16_group_id = orm.b_item_16_group_id,
        f_item_lab_type_id = orm.f_item_lab_type_id,
        b_specimen_id = orm.b_specimen_id
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
            item_printable = drug.item_printable,
            item_secret = drug.item_secret,
            b_item_16_group_id = drug.b_item_16_group_id,
            f_item_lab_type_id = drug.f_item_lab_type_id,
            b_specimen_id = drug.b_specimen_id
        )