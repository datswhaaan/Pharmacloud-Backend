from pydantic import BaseModel

class DeleteImagesRequest(BaseModel):
    images_id: list[str]