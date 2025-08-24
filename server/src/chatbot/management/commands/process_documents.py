from django.core.management.base import BaseCommand

import os
import re

from pdfminer.high_level import extract_text

from src.chatbot.adapters import ClientAdapter


class Command(BaseCommand):
    help = 'Process PDF documents and store embeddings'

    def handle(self, *args, **options):
        client = ClientAdapter.get_client()
        collection = ClientAdapter.get_collection()

        self.store_embeddings_and_chunks_into_db(client, collection)
        
        existing_count = collection.count()
        self.stdout.write(f"Collection currently has {existing_count} documents")

        self.stdout.write(
            self.style.SUCCESS('Successfully processed documents')
        )

    def store_embeddings_and_chunks_into_db(self, client, collection):
        raw_text = self.load_pdf_text()
        punctual_chunks = self.generate_chunks(
            raw_text, chunk_size=600, overlap=100)
        embeddings = self.generate_embeddings(punctual_chunks, client)

        ids = [f"chunk_{i}" for i in range(len(embeddings))]
        documents = list(embeddings.keys())
        embedding_vectors = list(embeddings.values())

        collection.add(
            embeddings=embedding_vectors,
            documents=documents,
            ids=ids
        )

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

    @staticmethod
    def load_pdf_text(filename="drf-react-gems.pdf"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, "docs", filename)

        return extract_text(pdf_path)
