from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2 import service_account

from app.domain.storage.storage import Storage

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleDriveStorage(Storage):
    def __init__(
        self,
        service_account_path: str,
        folder_id: str
    ):
        self.folder_id = folder_id

        creds = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=SCOPES
        )

        self.service = build("drive", "v3", credentials=creds)

    def upload(self, file, file_name: str) -> str:
        media = MediaInMemoryUpload(
            file.content,
            mimetype=file.content_type
        )

        file_metadata = {
            "name": file_name,
            "parents": [self.folder_id]
        }

        uploaded = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        return uploaded["id"]

    def get_public_url(self, file_id: str) -> str:
        return f"https://lh3.googleusercontent.com/d/{file_id}"

    def make_public(self, file_id: str) -> None:
        self.service.permissions().create(
            fileId=file_id,
            body={"role": "reader", "type": "anyone"}
        ).execute()

    def delete(self, file_id: str) -> None:
        self.service.files().delete(fileId=file_id).execute()