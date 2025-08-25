# import os
# import django

# # Point to your project’s settings module
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
# django.setup()

# import chromadb

# # Connect to Chroma (in-memory or persistent DB)
# client = chromadb.PersistentClient(path="chroma_data")

# # List all collections
# print(client.list_collections())

# # Get a collection
# collection = client.get_collection("drf_db")

# # Peek at what's stored
# items = collection.peek()  # shows a few records
# print(items)

# # Or fetch all (if dataset is small)
# all_items = collection.get()
# print(all_items.keys())      # ['ids', 'embeddings', 'documents', 'metadatas']
# print(all_items['documents'])  # your original texts



# # database = ClientAdapter()

# # chat_service = ChatService()

# # query = input("Please enter your question about the document: ")
# # print(f"\nUser Query: {query}")

# # document_service.store_embeddings_and_chunks_into_db()

# # query_embedding = document_service.generate_query_embedding(
# #     query, database.client)

# # if query_embedding:
# #     print(f"\nQuery Embedding (first 10 elements): {query_embedding[:10]}...")

# #     search_results = document_service.vector_search(
# #         query_embedding, database.collection, n_results=5)

# #     if search_results:
# #         ai_response = chat_service.generate_ai_response(
# #             query, search_results, database.client)

# #         if not ai_response:
# #             print("Failed to generate response.")
# #         else:
# #             print("Success.")
# #     else:
# #         print("No relevant information found in the document.")
# # else:
# #     print("Failed to generate query embedding.")
