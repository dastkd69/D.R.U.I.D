import spacy
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re

class TextProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')

    def determine_publication_venue(self, text):
        if re.search(r'IEEE', text, re.IGNORECASE):
            return 'IEEE'
        elif re.search(r'IEEE Access', text, re.IGNORECASE):
            return 'IEEE Access'
        elif re.search(r'MDPI', text, re.IGNORECASE):
            return 'MDPI'
        elif re.search(r'ACM', text, re.IGNORECASE):
            return 'ACM'
        else:
            return 'Other'

    def extract_entities_and_relationships(self, text):
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        relationships = [(token.text, token.dep_, token.head.text) for token in doc]
        return entities, relationships

    def extractive_summarize_text(self, text):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)  # Adjust the number of sentences in the summary
        return ' '.join(str(sentence) for sentence in summary)

    def abstractive_summarize_text(self, text):
        inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        outputs = self.model.generate(inputs, max_length=300, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(outputs[0])
        return summary

    def determine_publication_venue(self, text):
        if re.search(r'IEEE', text, re.IGNORECASE):
            return 'IEEE'
        elif re.search(r'IEEE Access', text, re.IGNORECASE):
            return 'IEEE Access'
        elif re.search(r'MDPI', text, re.IGNORECASE):
            return 'MDPI'
        elif re.search(r'ACM', text, re.IGNORECASE):
            return 'ACM'
        else:
            return 'Other'

    def summarize_text(self, text, method='extractive'):
        if method == 'extractive':
            return self.extractive_summarize_text(text)
        elif method == 'abstractive':
            return self.abstractive_summarize_text(text)
        else:
            raise ValueError("Invalid summarization method")

    def extract_topics(self, documents, n_topics=5):
        # Ensure that there are enough documents for max_df and min_df
        if all(len(doc.split()) <= 1 for doc in documents):
            return []

        # Adjust max_df and min_df based on the document length
        max_df = min(0.95, 1.0 / max(len(doc.split()) for doc in documents))
        min_df = max(1, 2)

        vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, stop_words='english')
        term_matrix = vectorizer.fit_transform(documents)
        lda = LatentDirichletAllocation(n_components=n_topics)
        lda.fit(term_matrix)
        topics = lda.components_
        return topics

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        return sentiment
