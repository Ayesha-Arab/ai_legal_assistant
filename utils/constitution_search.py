# utils/constitution_search.py
import re
from config import CONSTITUTION_PATH

# Load the constitution text
with open(CONSTITUTION_PATH, "r", encoding="utf-8") as f:
    constitution_text = f.read()

def search_constitution(query):
    """Search the Indian Constitution for articles or keywords."""
    if "article" in query.lower():
        article_num = re.search(r'article (\d+)', query, re.IGNORECASE)
        if article_num:
            article = f"Article {article_num.group(1)}"
            start = constitution_text.find(article)
            if start != -1:
                end = constitution_text.find("Article", start + 1) or len(constitution_text)
                return constitution_text[start:end].strip()
    keywords = query.split()
    for line in constitution_text.split('\n'):
        if all(keyword.lower() in line.lower() for keyword in keywords):
            return line.strip()
    return "No relevant information found in the Constitution."