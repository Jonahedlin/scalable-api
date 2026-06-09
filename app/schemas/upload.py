from typing import List, Literal
from pydantic import BaseModel


class UploadRecord(BaseModel):
    id: str
    name: str
    status: Literal["approved", "pending", "rejected"]
    submittedAt: str   # YYYY-MM-DD


class UploadsResponse(BaseModel):
    uploads: List[UploadRecord]
    hasMore: bool
    total: int


class UploadResponse(BaseModel):
    id: str
    name: str
    status: str
    submittedAt: str


class SubmissionCountResponse(BaseModel):
    count: int
