from app.domain.entities.drug import DrugImage, ImageVariantList
from app.domain.repositories.drug import DrugRepository
from app.application.dto.drug_dto import DrugDTO, DrugImageListDTO, DrugListDTO
from app.application.mappers.drug_mapper import _to_dto, _to_dto_list
from app.domain.entities.drug import DrugImageList, ImageVariantList

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

    def add_drug_image(self, drug_id: str, images: DrugImageList) -> None:
        variant_map = self.repository.get_variant_map()

        for image in images.images:
            print(type(image))
            if not image.view_type or not image.position or not image.lighting:
                raise ValueError("Each image must have view_type, position, and lighting defined.")
            image.variant_id = next(
                (variant.variant_id for variant in variant_map.variants
                    if variant.view_type == image.view_type and variant.position == image.position and variant.lighting == image.lighting),
                None
            )
            if image.variant_id is None:
                raise ValueError(f"Image variant not found for view_type={image.view_type}, position={image.position}, lighting={image.lighting}")

        self.repository.add_drug_image(drug_id, images)
