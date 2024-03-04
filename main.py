from downloaders import ArxivDownloader
from db import DatabaseManager
from processor import TextProcessor
from viz import KnowledgeGraph
from config import LOG_FILE, DB_NAME
from logger import setup_logger
import sqlite3

class PaperProcessor:
    def __init__(self, downloader, db_manager, text_processor, graph, logger):
        self.downloader = downloader
        self.db_manager = db_manager
        self.text_processor = text_processor
        self.graph = graph
        self.logger = logger

    def process_papers(self, search_terms):
        papers = self.downloader.fetch_papers(search_terms)
        for paper in papers:
            content = self.downloader.download_and_parse_paper(paper['link'])
            if content is not None:
                entities, relationships = self.text_processor.extract_entities_and_relationships(content)
                summary = self.text_processor.summarize_text(content)
                self.db_manager.store_paper(paper['link'], entities, relationships, summary)
                self.graph.add_entities(entities)
                self.graph.add_relationships(relationships)

        self.graph.visualize()

if __name__ == '__main__':
    logger = setup_logger(LOG_FILE)
    downloader = ArxivDownloader(logger)
    db_manager = DatabaseManager(logger)
    text_processor = TextProcessor()
    graph = KnowledgeGraph()
    processor = PaperProcessor(downloader, db_manager, text_processor, graph, logger)
    db_connection = sqlite3.connect(DB_NAME)
    processor.process_papers('machine unlearning')
