from fastapi import APIRouter, Depends, HTTPException
from app.presentation.schemas.drug import DrugSchema, DrugListSchema, DrugUpdateSchema
from app.presentation.dependencies import get_drug_service
from app.application.use_cases.drug_service import DrugService
from app.presentation.mappers.drug_mapper import _base_to_drug_dto

router = APIRouter(prefix="/drugs", tags=["drugs"])

@router.get("/{id}", response_model=DrugSchema)
def get_drug(
    id: str,
    service: DrugService = Depends(get_drug_service),
):
    try:
        drug = service.get_by_id(id)
        return drug
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=DrugListSchema)
def get_all_drugs(
    search: str | None = None,
    high_alert: bool | None = None,
    skip: int = 0,
    limit: int = 100,
    service: DrugService = Depends(get_drug_service),
):
    try:
        drug = service.get_all(search, high_alert=high_alert, skip=skip, limit=limit)
        return drug
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=DrugSchema)
def update_drug(
    id: str,
    drug: DrugUpdateSchema,
    service: DrugService = Depends(get_drug_service),
):
    try:
        dto = _base_to_drug_dto(id, drug)
        drug = service.update(dto)
        return drug
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))