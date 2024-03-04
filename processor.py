import spacy
from transformers import T5Tokenizer, T5ForConditionalGeneration
from collections import Counter

class TextProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')

    def extract_entities_and_relationships(self, text):
        doc = self.nlp(text)
        # Filter entities based on their type or relevance to your research topic
        entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'WORK_OF_ART']]
        # Count the frequency of each entity
        entity_freq = Counter([entity[0] for entity in entities])
        # Only keep the most common entities
        common_entities = [entity for entity, freq in entity_freq.items() if freq > 1]
        # Update the entities list
        entities = [entity for entity in entities if entity[0] in common_entities]
        # Extract relationships
        relationships = [(token.text, token.dep_, token.head.text) for token in doc]
        return entities, relationships

    def summarize_text(self, text):
        # Increase the max_length and min_length parameters to get a more detailed summary
        inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        outputs = self.model.generate(inputs, max_length=300, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(outputs[0])
        return summary
