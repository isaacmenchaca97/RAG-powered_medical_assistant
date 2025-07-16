import re
from urllib.parse import urlparse

from loguru import logger

from .base import BaseCrawler
from .custom_article import CustomArticleCrawler
from .pdf import PDFCrawler
from .pubmed import PubMedCrawler
from .pmc import PmcCrawler


class CrawlerDispatcher:
    def __init__(self) -> None:
        self._crawlers = {}

    @classmethod
    def build(cls) -> "CrawlerDispatcher":
        dispatcher = cls()

        return dispatcher

    def register_pdf(self) -> "CrawlerDispatcher":
        self.register("https://amazonaws.com", PDFCrawler)

        return self

    def register_pubmed(self) -> "CrawlerDispatcher":
        self.register("https://pubmed.ncbi.nlm.nih.gov", PubMedCrawler)

        return self

    def register_pmc(self) -> "CrawlerDispatcher":
        self.register("https://pmc.ncbi.nlm.nih.gov", PmcCrawler)

        return self

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        parsed_domain = urlparse(domain)
        domain = parsed_domain.netloc

        self._crawlers[
            r"https://((www\.)|(([a-zA-Z0-9.-]+)\.s3\.[a-zA-Z0-9-]+\.))?{}/*".format(
                re.escape(domain)
            )
        ] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()
        else:
            logger.warning(
                f"No crawler found for {url}. Defaulting to CustomArticleCrawler."
            )

            return CustomArticleCrawler()
