from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, Request
import json
from app.presentation.schemas.drug_response import  DrugResponse, DrugListResponse
from app.presentation.schemas.drug_request import DeleteImagesRequest
from app.presentation.dependencies import get_drug_service
from app.application.use_cases.drug_service import DrugService
from app.presentation.mappers.drug_mapper import _to_drug_image_list_dto, _to_drug_list_response, _to_drug_response, _to_drug_image_input_dto, _to_drug_image_list_response
from app.presentation.dependencies import get_current_user_id, limiter

router = APIRouter(prefix="/drugs", tags=["drugs"],
    dependencies=[Depends(get_current_user_id)])

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
@limiter.limit("5/minute")
async def add_drug_image(
    request: Request,
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
        
        valid_images = []
        errors = []

        for i, image in enumerate(images):
            try:
                if image.content_type not in ["image/jpeg", "image/png"]:
                    raise ValueError("Invalid file type")

                meta = metadata_list[i]

                drug_image = _to_drug_image_input_dto(
                    image=image,
                    view_type=meta.get("view_type") if meta else None,
                    position=meta.get("position") if meta else None,
                    lighting=meta.get("lighting") if meta else None
                )

                valid_images.append(drug_image)

            except Exception as e:
                errors.append({
                    "index": i,
                    "filename": image.filename,
                    "error": str(e)
                })

        drug_images = _to_drug_image_list_dto(drug_id, valid_images, trade_name)
        
        response = service.add_drug_image(drug_images, trade_name)
        
        return {
            "success": len(valid_images),
            "failed": len(errors),
            "errors": errors,
            "data": _to_drug_image_list_response(response) if response else None
        }
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