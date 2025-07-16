import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from loguru import logger
from llm_engineering.domain.documents import ArticleDocument
from .base import BaseCrawler
import requests


class PmcCrawler(BaseCrawler):
    model = ArticleDocument

    def __init__(self) -> None:
        super().__init__()

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article already exists in the database: {link}")
            return

        logger.info(f"Starting scrapping PMC article: {link}")

        # Extract PMC ID from the link (e.g., https://pmc.ncbi.nlm.nih.gov/articles/PMC9574204/)
        import re

        match = re.search(r"/articles/(PMC\d+)", link)
        if not match:
            logger.error(f"Could not extract PMC ID from link: {link}")
            return
        pmc_id = match.group(1)

        # Fetch article metadata and full text from NCBI E-utilities
        api_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {"db": "pmc", "id": pmc_id, "retmode": "xml"}
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        xml = response.text

        # Parse XML for title, journal, and full text
        root = ET.fromstring(xml)
        article = root.find(".//article")
        title = None
        journal = None
        full_text = None
        if article is not None:
            # Title
            title_el = article.find(".//article-title")
            title = title_el.text if title_el is not None else None
            # Journal
            journal_el = article.find(".//journal-title")
            journal = journal_el.text if journal_el is not None else None
            # Full text (concatenate all <p> tags in <body>)
            body = article.find(".//body")
            if body is not None:
                paragraphs = body.findall(".//p")
                full_text = "\n\n".join(
                    p.text for p in paragraphs if p is not None and p.text
                )

        content = {
            "Title": title,
            "Journal": journal,
            "Content": full_text,
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

        logger.info(f"Finished scrapping PMC article: {link}")
