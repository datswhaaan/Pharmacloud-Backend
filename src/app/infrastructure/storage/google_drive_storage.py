from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2 import service_account
import io
import os

from app.domain.storage.storage import Storage

SCOPES = ["https://www.googleapis.com/auth/drive"]
class GoogleDriveStorage(Storage):
    def __init__(self, credentials_path: str, folder_id: str):
        self.folder_id = folder_id
        self.creds = self._get_credentials(credentials_path)
        self.service = build("drive", "v3", credentials=self.creds)

    def _get_credentials(self, credentials_path: str):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    def upload(self, file, file_name: str) -> str:
        media = MediaIoBaseUpload(
            io.BytesIO(file.content),
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