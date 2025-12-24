from fastapi import APIRouter, Depends, HTTPException
from app.presentation.schemas.drug import DrugBase, DrugSchema, DrugListSchema
from app.presentation.dependencies import get_drug_service
from app.application.use_cases.drug_service import DrugService
from app.presentation.mappers.drug_mapper import _base_to_drug_dto, _schema_to_drug_dto

router = APIRouter(prefix="/drugs", tags=["drugs"])

@router.post("/", response_model=DrugSchema)
def create_drug(
    drug: DrugSchema,
    service: DrugService = Depends(get_drug_service),
):
    try:
        return service.create(_schema_to_drug_dto(drug))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{drug_code}", response_model=DrugSchema)
def get_drug(
    drug_code: str,
    service: DrugService = Depends(get_drug_service),
):
    try:
        
        drug = service.get_by_drug_code(drug_code)
        return drug
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=DrugListSchema)
def get_all_drugs(
    skip: int = 0,
    limit: int = 100,
    service: DrugService = Depends(get_drug_service),
):
    try:
        drug = service.get_all(skip=skip, limit=limit)
        return drug
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{drug_code}", response_model=DrugSchema)
def update_drug(
    drug_code: str,
    drug: DrugBase,
    service: DrugService = Depends(get_drug_service),
):
    try:
        dto = _base_to_drug_dto(drug_code, drug)
        drug = service.update(dto)
        return drug
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{drug_code}", status_code=204)
def delete_drug(
    drug_code: str,
    service: DrugService = Depends(get_drug_service),
):
    try:
        service.delete(drug_code)
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))