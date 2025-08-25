import json
import os

from rest_framework.response import Response
from rest_framework import status

from src.chatbot.constants import ERROR_RESPONSE_OBJECT


class ContextProcessingMixin:
    """Provides utilities for generating embeddings, performing vector searches, 
    and preparing contextual data for query processing."""

    @staticmethod
    def generate_query_embedding(query_text, client, model="text-embedding-ada-002"):
        """Generate an embedding vector for the given query text using the specified model."""

        try:
            response = client.embeddings.create(
                input=[query_text],
                model=model
            )
            if response.data and len(response.data) > 0:
                return response.data[0].embedding
            else:
                print("Warning: No embedding returned for the query.")
                return None
        except Exception as e:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def vector_search(query_embedding, collection, n_results=5):
        """Perform a vector similarity search in the collection based on the query embedding."""

        if query_embedding is None:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents'],
            )

            if results and results.get('documents') and results['documents'][0]:
                return results['documents'][0]
            else:
                print("No results found for the query.")
                return []

        except Exception as e:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FileStorageMixin:
    def save_memory(self, key: str, value: str):
        """Store a key-value pair in memory file with robust error handling"""

        memory = {}

        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    content = f.read().strip()
                    memory = json.loads(content)
            except Exception as e:
                memory = {}

        memory[key] = value

        try:
            with open(self.memory_file, "w") as f:
                json.dump(memory, f, indent=2)
            return "Stored successfully"
        except Exception as e:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def load_memory(self, query: str):
        """Search for stored memories matching the query with robust error handling"""

        if not os.path.exists(self.memory_file):
            return "No memories stored"

        try:
            with open(self.memory_file, "r") as f:
                content = f.read().strip()
                if not content:
                    return "No memories stored"

                memory = json.loads(content)
                if not memory:
                    return "No memories stored"

                return json.dumps(memory, indent=2)

        except json.JSONDecodeError as e:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def load_chat_history(self):
        """Load chat history from JSON file."""

        if os.path.exists(self.chat_history_file):
            try:
                with open(self.chat_history_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_chat_history(self, history):
        """Save chat history to JSON file."""

        try:
            with open(self.chat_history_file, "w") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
