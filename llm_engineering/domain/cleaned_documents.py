from abc import ABC

from pydantic import UUID4

from .base import VectorBaseDocument
from .types import DataCategory


class CleanedDocument(VectorBaseDocument, ABC):
    content: str
    platform: str
    author_id: UUID4
    author_full_name: str


class CleanedArticleDocument(CleanedDocument):
    link: str

    class Config:
        name = "cleaned_articles"
        category = DataCategory.ARTICLES
        use_vector_index = False


class CleanedPdfDocument(CleanedDocument):
    link: str

    class Config:
        name = "cleaned_pdf"
        category = DataCategory.PDF
        use_vector_index = False
