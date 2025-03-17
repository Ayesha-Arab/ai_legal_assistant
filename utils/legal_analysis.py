# utils/legal_analysis.py
from transformers import pipeline

# Using a general NER pipeline as legal-bert-small-uncased isn't fine-tuned for NER by default
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")  # Fallback; adjust if legal-specific NER is needed

def analyze_legal_document(text):
    """Analyze legal document text and extract entities."""
    entities = ner_pipeline(text[:512])  # Limit to 512 tokens due to BERT constraints
    analysis = {
        "entities": [{"word": ent["word"], "label": ent["entity"]} for ent in entities]
    }
    return analysis