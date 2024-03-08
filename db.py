import sqlite3

class DatabaseManager:
    def __init__(self, db_name, logger):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.logger = logger
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY,
                link TEXT,
                title TEXT,
                abstract TEXT,
                authors TEXT,
                publication_venue TEXT,
                keywords TEXT,
                entities TEXT,
                relationships TEXT,
                extractive_summary TEXT,
                abstractive_summary TEXT,
                topics TEXT,
                sentiment REAL
            )
        """)

        self.conn.commit()

    def store_paper(self, link, publication_venue,
                    entities, relationships, extractive_summary, abstractive_summary,
                    topics, sentiment):
        try:
            self.cursor.execute("""
                INSERT INTO papers (link, publication_venue, 
                                    entities, relationships, extractive_summary, abstractive_summary,
                                    topics, sentiment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (link, publication_venue, 
                  entities, relationships, extractive_summary, abstractive_summary,
                  topics, sentiment))

            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"An error occurred: {e.args[0]}")


    def update_paper_topics(self, link, topics):
        try:
            self.cursor.execute("""
                UPDATE papers
                SET topics = ?
                WHERE link = ?
            """, (topics, link))

            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"An error occurred: {e.args[0]}")