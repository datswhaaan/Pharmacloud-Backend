from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os

from app.domain.storage.storage import Storage

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleDriveStorage(Storage):
    def __init__(
        self,
        credentials_path: str,
        token_path: str,
        folder_id: str
    ):
        self.folder_id = folder_id
        self.credentials_path = credentials_path
        self.token_path = token_path

        creds = self._get_credentials()

        self.service = build("drive", "v3", credentials=creds)

    def _get_credentials(self) -> Credentials:
        creds = None

        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(
                self.token_path, SCOPES
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return creds

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