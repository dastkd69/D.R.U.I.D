import requests
from bs4 import BeautifulSoup
from config import BASE_URL
from logger import setup_logger
from urllib.parse import quote


class ArxivDownloader:
    def __init__(self, logger):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.logger = logger

    def fetch_papers(self, search_terms):
        query = 'search_query=all:' + quote(search_terms)
        response = self.session.get(self.base_url + query).content
        feed = BeautifulSoup(response, 'xml')
        papers = [{'title': entry.title.text, 'authors': entry.author.text, 'summary': entry.summary.text,
                   'link': entry.id.text} for entry in feed.find_all('entry')]
        return papers

    def download_and_parse_paper(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to download paper: {url}')
            self.logger.error(e)
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()
        return content
