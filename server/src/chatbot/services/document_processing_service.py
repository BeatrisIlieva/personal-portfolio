
import os
import re

from pdfminer.high_level import extract_text

from src.chatbot.services.database_service import DatabaseService


class DocumentProcessingService(DatabaseService):
    @staticmethod
    def generate_chunks(text, chunk_size=500, overlap=100):
        split_points = r'(?<=[.!?;\n])\s*'
        sentences = re.split(split_points, text)

        chunks = []
        current_chunk = ""
        i = 0
        while i < len(sentences):
            sentence = sentences[i]

            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence
                i += 1
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    overlap_start = max(0, len(current_chunk) - overlap)
                    current_chunk = current_chunk[overlap_start:] + sentence
                    i += 1
                else:
                    chunks.append(sentence[:chunk_size].strip())
                    sentences[i] = sentence[chunk_size:]
                    if not sentences[i]:
                        i += 1

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    @staticmethod
    def generate_embeddings(chunks, client, model="text-embedding-ada-002"):
        chunk_embeddings = {}

        try:
            response = client.embeddings.create(
                input=chunks,
                model=model
            )
            for i, chunk in enumerate(chunks):
                if i < len(response.data):
                    chunk_embeddings[chunk] = response.data[i].embedding
                else:
                    print(f"Warning: No embedding returned for chunk {i+1}.")

            return chunk_embeddings
        except Exception as e:
            print(f"An error occurred during embedding generation: {e}")
            return None

    def store_embeddings_and_chunks_into_db(self):
        raw_text = self.load_pdf_text()
        punctual_chunks = self.generate_chunks(
            raw_text, chunk_size=600, overlap=100)
        embeddings = self.generate_embeddings(punctual_chunks, self.client)

        ids = [f"chunk_{i}" for i in range(len(embeddings))]
        documents = list(embeddings.keys())
        embedding_vectors = list(embeddings.values())

        self.collection.add(
            embeddings=embedding_vectors,
            documents=documents,
            ids=ids
        )

    @staticmethod
    def load_pdf_text(filename="drf-react-gems.pdf"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, "docs", filename)

        return extract_text(pdf_path)

    @staticmethod
    def generate_query_embedding(query_text, client, model="text-embedding-ada-002"):
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
            print(f"An error occurred during query embedding generation: {e}")
            return None

    @staticmethod
    def vector_search(query_embedding, collection, n_results=5, distance_threshold=None):
        if query_embedding is None:
            print("Error: Query embedding is None.")
            return None, None

        try:
            where_clause = {}
            if distance_threshold is not None:
                where_clause = {"distance": {"$lt": distance_threshold}}

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'distances'],
                # where=where_clause
            )

            if results and results.get('documents') and results['documents'][0]:
                return results['documents'][0], results['distances'][0]
            else:
                print("No results found for the query.")
                return [], []

        except Exception as e:
            print(f"An error occurred during vector search: {e}")
            return None, None
