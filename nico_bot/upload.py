import os
from pathlib import Path
from typing import Optional

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFile


def upload_drive(file_path: str, credential_json: Optional[str] = None,
                 drive_directory: Optional[str] = None) -> GoogleDriveFile:
    if not credential_json:
        credential_json = os.environ["GCP_SERVICE_ACCOUNT"]
    if not drive_directory:
        drive_directory = os.environ["GOOGLE_DRIVE_PATH"]

    settings = {
        "client_config_backend": "service",
        "service_config": {
            "client_json_file_path": credential_json,
        },
    }
    gauth = GoogleAuth(settings=settings)
    gauth.ServiceAuth()
    drive = GoogleDrive(gauth)
    drive_file = drive.CreateFile({"title": Path(file_path).name, "parents": [{"id": drive_directory}]})
    drive_file.SetContentFile(os.path.abspath(file_path))
    drive_file.Upload()
    return drive_file
