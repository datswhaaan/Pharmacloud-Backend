import os
from dotenv import load_dotenv
import requests

load_dotenv()

INFERENCE_API_KEY=os.getenv("INFERENCE_API_KEY")
class MedicationVisionAPIClient:
    def __init__(self, url: str):
        self.base_url = url
    def predict(self, image_bytes: bytes):
        url = f"{self.base_url}"

        file = {
            "file": ("image.jpg", image_bytes, "image/jpeg")
        }

        headers = {
            "Authorization": INFERENCE_API_KEY
        }

        try:
            response = requests.post(
                url,
                files=file,
                headers=headers,
                timeout=60,
            )

            if response.status_code != 200:
                raise Exception(f"Inference API error: {response.text}")

            return response.json()

        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")