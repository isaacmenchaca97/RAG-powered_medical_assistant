from abc import ABC

from pydantic import UUID4, Field

from llm_engineering.domain.base import VectorBaseDocument
from llm_engineering.domain.types import DataCategory


class Chunk(VectorBaseDocument, ABC):
    content: str
    platform: str
    document_id: UUID4
    author_id: UUID4
    author_full_name: str
    metadata: dict = Field(default_factory=dict)


class ArticleChunk(Chunk):
    link: str

    class Config:
        category = DataCategory.ARTICLES


class PdfChunk(Chunk):
    link: str

    class Config:
        category = DataCategory.PDF
