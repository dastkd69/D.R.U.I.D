import spacy

def extract_entities_and_relationships(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    entities = [(ent.text, ent.label_) for ent in doc.ents]
    relationships = [(token.text, token.dep_, token.head.text) for token in doc]

    return entities, relationships
