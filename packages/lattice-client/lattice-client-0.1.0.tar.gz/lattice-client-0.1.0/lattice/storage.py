import gzip
import http.client
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional
from uuid import uuid4

import requests

from .utils import create_access_token_header, create_token_header

_PLATFORM_CORE_PUBLIC_API_HOST = "https://public.lattice.ensquared.co.uk/core"
_PLATFORM_CORE_PRIVATE_API_HOST = (
    "https://s3pnua7j7d.execute-api.eu-west-2.amazonaws.com/v1"
)
_TEMPORARY_STORAGE_PATH = os.environ.get("TEMPORARY_STORAGE_PATH", "/tmp")


class File:
    _id: str
    _path: str
    _name: str

    def __init__(self, path: str, *, name: Optional[str] = None):
        self._id = str(uuid4())
        self._path = path
        self._name = name or os.path.basename(path)

    def __str__(self) -> str:
        return self.path

    def get_path(self, api_key: Optional[str] = None) -> str:
        return self._download(api_key=api_key)

    @property
    def path(self) -> str:
        return self.get_path()

    @staticmethod
    def _get_authentication_header(api_key: Optional[str]):
        if api_key is not None:
            return create_token_header(api_key)

        if (machine_token := os.environ.get("MACHINE_TOKEN")) is not None:
            return create_access_token_header(machine_token)

        raise ValueError(
            "No access token found in the environment. "
            "Is this a valid platform lattice runtime?"
        )

    def _execute(
        self,
        path: str,
        data: dict,
        *,
        host: str,
        api_key: Optional[str] = None,
    ):
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "authorization": self._get_authentication_header(api_key),
        }

        response = requests.post(
            f"{host}/{path}",
            headers=headers,
            json=data,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                f"Request failed with status {response.status_code}: {response.text}"
            )

    def _download(self, *, api_key: Optional[str] = None):
        object_data = self._execute(
            "objects/get_object",
            {"tenant_id": "lattice", "id": self._id},
            host=_PLATFORM_CORE_PRIVATE_API_HOST,
            api_key=api_key,
        )
        with urllib.request.urlopen(object_data["get_url"]) as response:
            object_bytes = response.read()
            object_path = os.path.join(_TEMPORARY_STORAGE_PATH, self._name)
            with open(object_path, "wb") as file:
                file.write(gzip.decompress(object_bytes))
                return object_path

    def download(self, *, api_key: str):
        self._download(api_key=api_key)

    def _upload(
        self,
        data: bytes,
        *,
        execution_id: str,
        path: str,
        api_key: Optional[str] = None,
    ):
        name = os.path.basename(path)

        response = self._execute(
            "create_upload",
            data={
                "id": self._id,
                "name": name,
                "size": len(data),
                "hash": "test",
                "execution_id": execution_id,
            },
            host=_PLATFORM_CORE_PUBLIC_API_HOST,
            api_key=api_key,
        )

        boundary = f"------------------------{uuid4()}"
        body = []

        post_data = json.loads(response["upload"]["post_data"])
        post_url = post_data["url"]
        post_fields = post_data["fields"]

        for key, value in post_fields.items():
            body.append(f"--{boundary}")
            body.append(f'Content-Disposition: form-data; name="{key}"')
            body.append("")
            body.append(value.encode("utf-8"))

        # Add the file to be uploaded
        body.append(f"--{boundary}")
        body.append(
            'Content-Disposition: form-data; name="file"; filename="your_filename.ext"'
        )
        body.append("Content-Type: application/octet-stream")
        body.append("")
        body.append(gzip.compress(data))

        # End the request body with the boundary
        body.append(f"--{boundary}--")
        body.append("")

        # Join all the parts of the body into a single string
        body = [
            part.encode("utf-8") if isinstance(part, str) else part for part in body
        ]
        body = b"\r\n".join(body)

        parsed_url = urllib.parse.urlsplit(post_url)
        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        }

        connection = http.client.HTTPSConnection(parsed_url.netloc)
        try:
            connection.request("POST", parsed_url.path, body, headers)
            response = connection.getresponse()
            response_data = response.read().decode()

            if response.status == 204 or response.status == 200:
                print(f"{self._name} uploaded successfully.")
            else:
                print(f"Upload failed with status {response.status}: {response_data}")
        finally:
            connection.close()

    def upload(self, *, execution_id: str, api_key: str):
        with open(self._path, "rb") as file:
            data = file.read()
            self._upload(
                data,
                execution_id=execution_id,
                path=self._path,
                api_key=api_key,
            )
