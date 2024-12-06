import mimetypes
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel


class Batch(BaseModel):
    id: int
    uid: str
    name: str
    status: str
    project_id: int
    created_at: str
    updated_at: str


class Document(BaseModel):
    id: int
    uid: str
    display_name: str
    value: Dict[str, Any]
    file_hash: str
    gcs_path: str
    user_id: Optional[int] = None
    status: str
    created_at: str
    updated_at: str


class UploadDocumentsResponse(BaseModel):
    batch: Batch
    documents: List[Document]


def guess_mime_type(filename: str) -> str:
    """Guess content type from filename."""
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or "application/octet-stream"


def is_valid_file_upload_file(file_obj):
    """
    Check if a file upload object satisfies the requirements of both FileStorage and UploadFile.

    Args:
        file_obj (Union[werkzeug.datastructures.FileStorage, starlette.datastructures.UploadFile]): The file upload object to be checked.

    Returns:
        bool: True if the object has the necessary attributes, False otherwise.
    """
    return all(
        [
            hasattr(file_obj, "filename"),
            hasattr(file_obj, "file"),
        ]
    )


def is_valid_file_object(file_obj):
    """
    Check if a file object is a valid Python file-like object (e.g. SpooledTemporaryFile, BufferedReader, etc.).

    Args:
        file_obj (object): The file object to be checked.

    Returns:
        bool: True if the object is a valid file-like object, False otherwise.
    """
    return all(
        [
            hasattr(file_obj, "read"),
            hasattr(file_obj, "seek"),
            hasattr(file_obj, "tell"),
        ]
    )


class Documents:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    def upload(self, files: List[Any]):
        files_to_upload = []
        for file in files:
            if is_valid_file_upload_file(file):
                filename = file.filename or f"temp-{uuid4()}"
                filestream = file.file
            elif is_valid_file_object(file):
                filename = Path(getattr(file, "name", f"temp-{uuid4()}")).name
                filestream = file

            file_type = guess_mime_type(filename)

            if hasattr(filestream, "read"):
                files_to_upload.append(("documents", (filename, filestream, file_type)))
            else:
                raise ValueError("Only file uploads are supported")

        response = self.client.post(
            f"{self.base_url}/public/v1/documents", files=files_to_upload
        )
        response.raise_for_status()
        return UploadDocumentsResponse(**response.json())


class DocumentsAsync:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    async def upload(self, files: List[Any]):
        files_to_upload = []
        for file in files:
            if is_valid_file_upload_file(file):
                filename = file.filename or f"temp-{uuid4()}"
                filestream = file.file
            elif is_valid_file_object(file):
                filename = Path(getattr(file, "name", f"temp-{uuid4()}")).name
                filestream = file

            file_type = guess_mime_type(filename)

            if hasattr(filestream, "read"):
                files_to_upload.append(("documents", (filename, filestream, file_type)))
            else:
                raise ValueError("Only file uploads are supported")

        response = await self.client.post(
            f"{self.base_url}/public/v1/documents", files=files_to_upload
        )
        response.raise_for_status()
        return UploadDocumentsResponse(**response.json())
