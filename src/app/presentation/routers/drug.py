from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
import json
from app.presentation.schemas.drug_response import  DrugResponse, DrugListResponse
from app.presentation.schemas.drug_request import DeleteImagesRequest
from app.presentation.dependencies import get_drug_service
from app.application.use_cases.drug_service import DrugService
from app.presentation.mappers.drug_mapper import _to_drug_image_list_dto, _to_drug_list_response, _to_drug_response, _to_drug_image_input_dto, _to_drug_image_list_response

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
    trade_name: str,
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

            drug_image = _to_drug_image_input_dto(
                            image=image,
                            view_type=meta.get("view_type") if meta else None,
                            position=meta.get("position") if meta else None,
                            lighting=meta.get("lighting") if meta else None
                        )

            image_objs.append(drug_image)

        drug_images = _to_drug_image_list_dto(drug_id, image_objs, trade_name)
        
        response = service.add_drug_image(drug_images, trade_name)
        
        return _to_drug_image_list_response(response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/images")
def delete_drug_image(
    image_ids: DeleteImagesRequest,
    service: DrugService = Depends(get_drug_service),
):
    try:
        service.delete_drug_image(image_ids.image_ids)
        return {
            "message": "Images deleted successfully",
            "deleted_ids": image_ids.image_ids
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))