from loguru import logger
from llm_engineering.domain.documents import PDFDocument
from .base import BaseCrawler
from urllib.parse import urlparse
import requests
from pypdf import PdfReader
from io import BytesIO
from llm_engineering.application.utils import deidentify_text


class PDFCrawler(BaseCrawler):
    model = PDFDocument

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article already exists in the database: {link}")
            return

        logger.info(f"Starting scrapping S3 PDF: {link}")

        # Download PDF
        response = requests.get(link)
        response.raise_for_status()

        # Read PDF content
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)

        # De-identify text
        text = deidentify_text(text)

        # Prepare content dict
        content = {
            "Title": None,  # PDF metadata title could be extracted if needed
            "Content": text,
        }

        parsed_url = urlparse(link)
        platform = parsed_url.netloc

        user = kwargs["user"]
        instance = self.model(
            content=content,
            link=link,
            platform=platform,
            author_id=user.id,
            author_full_name=user.full_name,
        )
        instance.save()

        logger.info(f"Finished scrapping PDF: {link}")
