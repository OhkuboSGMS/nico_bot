import os
from io import StringIO
from typing import Optional, IO

from dotenv import load_dotenv
from google.cloud.secretmanager import SecretManagerServiceClient


def secret_variables(credential_json: Optional[str] = None, path: Optional[str] = None, encoding="UTF-8"):
    if not credential_json:
        credential_json = os.environ["GCP_SERVICE_ACCOUNT"]
    if not path:
        path = os.environ["SM_PATH"]
    client = SecretManagerServiceClient.from_service_account_file(credential_json)
    result = client.access_secret_version(name=path).payload.data.decode(encoding)
    return result


def load_dict_as_environment_variables(data: dict):
    for key, value in data.items():
        os.environ[key] = str(value)


def load_env(env_file_io: IO):
    load_dotenv(stream=env_file_io)


def load_secret_variables(credential_json: Optional[str] = None, versions=(), encoding="UTF-8"):
    data = secret_variables(credential_json, versions, encoding)
    load_env(StringIO(data))
