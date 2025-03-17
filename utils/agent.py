# utils/agent.py
from groq import Groq
from config import GROQ_API_KEY
from utils.constitution_search import search_constitution

class LegalAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.base_prompt = (
            "You are an AI-powered Legal Research Assistant specializing in Indian law, designed to assist lawyers, students, and researchers. "
            "Provide accurate, concise, and legally informed responses based on the Indian Penal Code (IPC), Motor Vehicles Act, or other relevant Indian laws. "
            "For queries about accidents or crimes: "
            "1. Identify the type of crime (e.g., negligence, rash driving, causing hurt). "
            "2. Cite specific IPC sections, Motor Vehicles Act provisions, or constitutional articles if applicable. "
            "3. Explain potential punishments (imprisonment, fines, or both) under Indian law. "
            "Use the provided context or constitution text if relevant. "
            "If unsure, state limitations and suggest consulting a legal professional. "
            "Keep responses clear and focused on Indian legal consequences."
        )

    def query_groq(self, user_input, context=""):
        """Query Groq API with user input and optional context."""
        full_prompt = f"{self.base_prompt}\n\nContext: {context}\nUser Query: {user_input}"
        try:
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Check Groq docs for available models
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error with Groq API: {str(e)}"

    def handle_query(self, user_input, document_text=None):
        """Handle user queries with context from documents or constitution."""
        if "article" in user_input.lower() or "constitution" in user_input.lower():
            return search_constitution(user_input)
        elif document_text:
            context = document_text[:1000]  # Limit context to avoid token limits
            return self.query_groq(user_input, context)
        else:
            return self.query_groq(user_input)

# Example usage (for testing)
if __name__ == "__main__":
    agent = LegalAgent()
    print(agent.handle_query("What if I accidentally hit some person?"))
    print(agent.handle_query("What is negligence?", document_text="Negligence involves duty of care..."))