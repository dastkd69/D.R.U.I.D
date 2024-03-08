# main.py

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

    def process_papers(self, search_terms, max_papers=25):
        papers = self.downloader.fetch_papers(search_terms)[:max_papers]
        all_content = []  # Accumulate content of all papers
        all_entities = []  # Accumulate entities of all papers
        all_sentiments = []  # Accumulate sentiments of all papers

        for paper in papers:
            content = self.downloader.download_and_parse_paper(paper['link'])
            if content is not None:
                all_content.append(content)

                entities, relationships = self.text_processor.extract_entities_and_relationships(content)
                all_entities.extend(entities)  # Add entities to all_entities list
                extractive_summary = self.text_processor.extractive_summarize_text(content)
                abstractive_summary = self.text_processor.abstractive_summarize_text(content)
                sentiment = self.text_processor.analyze_sentiment(content)
                all_sentiments.append(sentiment)  # Add sentiment to all_sentiments list
                venue = self.text_processor.determine_publication_venue(content)

                self.db_manager.store_paper(
                    link=paper['link'],
                    entities=entities,
                    relationships=relationships,
                    extractive_summary=extractive_summary,
                    abstractive_summary=abstractive_summary,
                    publication_venue=venue,
                    sentiment=sentiment,
                    topics=[],  # Empty for now; topics will be extracted after accumulating all content                    
                )
                self.graph.add_entities(entities)
                self.graph.add_relationships(relationships)

        # Extract topics after accumulating all content
        all_content = ' '.join(all_content)
        topics = self.text_processor.extract_topics(all_content)
        
        # Update the stored papers with the extracted topics
        for paper in papers:
            self.db_manager.update_paper_topics(paper['link'], topics)

        # Visualize the graph
        self.graph.visualize_graph()

        # Visualize word cloud
        self.graph.visualize_wordcloud(all_entities)

        # Visualize sentiment pie chart
        self.graph.visualize_sentiment_pie(all_sentiments)



logger = setup_logger(LOG_FILE)
downloader = ArxivDownloader(logger)
db_manager = DatabaseManager(DB_NAME, logger)
text_processor = TextProcessor()
graph = KnowledgeGraph()
processor = PaperProcessor(downloader, db_manager, text_processor, graph, logger)  # Use the correct class
db_connection = sqlite3.connect(DB_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph')
def display_graph():
    if os.path.exists('graph.html'):
        return send_file('graph.html', mimetype='text/html')
    else:
        return "No graph available", 404

@app.route('/process', methods=['POST'])
def process():
    search_terms = request.form['search_terms']
    start = time.time()
    processor.process_papers(search_terms)
    end = time.time()
    processing_time = end - start
    logger.info(f"Processing took {processing_time} seconds")
    return redirect(url_for('display_graph'))

if __name__ == '__main__':
    app.run(debug=True)
