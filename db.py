import os
import sqlite3
from config import DB_NAME

class DatabaseManager:
    def __init__(self, logger):
        self.db_connection = sqlite3.connect(DB_NAME)
        self.logger = logger

        # Create the table if it doesn't exist
        self.create_table()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                url TEXT PRIMARY KEY,
                entities TEXT,
                relationships TEXT,
                summary TEXT
            )
        """)
        self.db_connection.commit()

    def store_paper(self, url, entities, relationships, summary):
        try:
            entities_str = str(entities)
            relationships_str = str(relationships)
            summary_str = str(summary)

            # Store the data in the database
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO papers (url, entities, relationships, summary) VALUES (?, ?, ?, ?)",
                           (url, entities_str, relationships_str, summary_str))
            self.db_connection.commit()

            self.logger.info(f'Successfully parsed and stored paper: {url}')
        except Exception as e:
            self.logger.error(f'Failed to parse or store paper: {url}')
            self.logger.error(e)
