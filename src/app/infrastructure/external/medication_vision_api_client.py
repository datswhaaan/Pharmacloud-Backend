import requests

class MedicationVisionAPIClient:
    def __init__(self, url: str):
        self.base_url = url

    def predict(self, image_bytes: bytes):
        url = f"{self.base_url}/predict"
        file = {"file": ("image.jpg", image_bytes, "image/jpeg")}
        try:
            response = requests.post(
                url,
                files=file,
                timeout=10,
            )

            if response.status_code != 200:
                raise Exception(f"Inference API error: {response.text}")

            return response.json()

        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")