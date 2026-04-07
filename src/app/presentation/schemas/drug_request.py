from pydantic import BaseModel

class DeleteImagesRequest(BaseModel):
    image_ids: list[str]