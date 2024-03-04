from flask import Flask, render_template, request, send_file, redirect, url_for
from downloaders import ArxivDownloader
from db import DatabaseManager
from processor import TextProcessor
from viz import KnowledgeGraph
from config import LOG_FILE, DB_NAME
from logger import setup_logger
import sqlite3
import os
import time


app = Flask(__name__)

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


logger = setup_logger(LOG_FILE)
downloader = ArxivDownloader(logger)
db_manager = DatabaseManager(logger)
text_processor = TextProcessor()
graph = KnowledgeGraph()
processor = PaperProcessor(downloader, db_manager, text_processor, graph, logger)
db_connection = sqlite3.connect(DB_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph')
def graph():
    if os.path.exists('graph.png'):
        return send_file('graph.html', mimetype='text/html')
    else:
        return "No graph available", 404

@app.route('/process', methods=['POST'])
def process():
    search_terms = request.form['search_terms']
    start = time.time()
    processor.process_papers(search_terms)
    end = time.time()
    print(f"Processing took {end - start} seconds")
    logger.info(f"Processing took {end - start} seconds")
    return redirect(url_for('graph'))

if __name__ == '__main__':
    app.run()


