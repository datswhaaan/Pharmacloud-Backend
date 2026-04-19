from app.domain.repositories.drug import DrugRepository
from app.application.mappers.drug_mapper import _to_dto, _to_dto_list, _to_drug_image_upload, _to_drug_image_list_upload, _to_drug_image_list_dto
from app.application.dto.drug_dto import DrugDTO, DrugListDTO, DrugImageListInputDTO, DrugImageListDTO

class DrugService:
    def __init__(self, repository: DrugRepository):
        self.repository = repository

    def get_by_id(self, id: str) -> DrugDTO | None:
        drug = self.repository.get_by_id(id)
        if drug is None:
            return None
        return _to_dto(drug)

    def get_all(
        self,
        search: str | None = None,
        *,
        high_alert: bool | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> DrugListDTO:
        drugs = self.repository.get_all(search, high_alert=high_alert, skip=skip, limit=limit)
        return _to_dto_list(drugs)

    def add_drug_image(self, images: DrugImageListInputDTO, trade_name: str) -> DrugImageListDTO:
        variant_map = self.repository.get_variant_map()
        image_objs = []

        for image in images.images:
            if not image.view_type or not image.position or not image.lighting:
                raise ValueError("Each image must have view_type, position, and lighting defined.")
            variant_id = next(
                (variant.variant_id for variant in variant_map.variants
                    if variant.view_type == image.view_type and variant.position == image.position and variant.lighting == image.lighting),
                None
            )
            if variant_id is None:
                raise ValueError(f"Image variant not found for view_type={image.view_type}, position={image.position}, lighting={image.lighting}")
            
            image_objs.append(_to_drug_image_upload(image, variant_id))

        drug_images = self.repository.add_drug_image(images.b_item_id, trade_name, _to_drug_image_list_upload(images.b_item_id, image_objs))

        return _to_drug_image_list_dto(drug_images)
    
    def delete_drug_image(self, image_ids: list[str]) -> None:
        return self.repository.delete_drug_image(image_ids)