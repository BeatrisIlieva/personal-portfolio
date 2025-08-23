from django.conf import settings

import openai
import chromadb


class DatabaseService:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(
            "portfolio_db"
        )
