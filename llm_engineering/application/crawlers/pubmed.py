from urllib.parse import urlparse
from loguru import logger
from llm_engineering.domain.documents import ArticleDocument
from .base import BaseCrawler
import requests
import xml.etree.ElementTree as ET


class PubMedCrawler(BaseCrawler):
    model = ArticleDocument

    def __init__(self) -> None:
        super().__init__()

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article already exists in the database: {link}")
            return

        logger.info(f"Starting scrapping PubMed article: {link}")

        # Extract PubMed ID from the link
        import re

        match = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", link)
        if not match:
            logger.error(f"Could not extract PubMed ID from link: {link}")
            return
        pubmed_id = match.group(1)

        # Fetch article metadata from NCBI E-utilities
        api_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {"db": "pubmed", "id": pubmed_id, "retmode": "xml"}
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        xml = response.text

        # Parse XML for title, abstract, etc.
        root = ET.fromstring(xml)
        article = root.find(".//Article")
        title = article.findtext("ArticleTitle") if article is not None else None
        abstract = (
            article.findtext("Abstract/AbstractText") if article is not None else None
        )
        journal = article.findtext("Journal/Title") if article is not None else None
        language = article.findtext("Language") if article is not None else None

        # De-identify abstract text
        # if abstract:
        #     abstract = deidentify_text(abstract)

        content = {
            "Title": title,
            "Journal": journal,
            "Content": abstract,
            "language": language,
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

        logger.info(f"Finished scrapping PubMed article: {link}")
