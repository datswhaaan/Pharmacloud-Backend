from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
import json
from app.presentation.schemas.drug_response import  DrugResponse, DrugListResponse
from app.presentation.dependencies import get_drug_service
from app.application.use_cases.drug_service import DrugService
from app.presentation.mappers.drug_mapper import _to_drug_image_list_dto, _to_drug_list_response, _to_drug_response, _to_drug_image_input_dto

router = APIRouter(prefix="/drugs", tags=["drugs"])

@router.get("/{id}", response_model=DrugResponse)
def get_drug(
    id: str,
    service: DrugService = Depends(get_drug_service),
):
    try:
        drug = service.get_by_id(id)
        return _to_drug_response(drug)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=DrugListResponse)
def get_all_drugs(
    search: str | None = None,
    high_alert: bool | None = None,
    skip: int = 0,
    limit: int = 7,
    service: DrugService = Depends(get_drug_service),
):
    try:
        drug = service.get_all(search, high_alert=high_alert, skip=skip, limit=limit)
        return _to_drug_list_response(drug)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/{drug_id}/images")
async def add_drug_image(
    drug_id: str,
    images: list[UploadFile],
    metadatas: str = Form(...),
    service: DrugService = Depends(get_drug_service),
):
    try:
        metadata_list = json.loads(metadatas)

        if len(metadata_list) != len(images):
            raise HTTPException(
                status_code=400,
                detail="images and metadatas length mismatch"
            )
        
        image_objs = []

        for i, image in enumerate(images):
            meta = metadata_list[i]

            image_objs.append(
                _to_drug_image_input_dto(
                    image=image,
                    view_type=meta.get("view_type"),
                    position=meta.get("position"),
                    lighting=meta.get("lighting")
                )
            )

        drug_images = _to_drug_image_list_dto(drug_id, image_objs)
        
        service.add_drug_image(drug_images)
        return {"message": "Images added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))