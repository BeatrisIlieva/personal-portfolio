# # import os
# # import json

# # from rest_framework.response import Response
# # from rest_framework import status

# # from src.chatbot.constants import ERROR_RESPONSE_OBJECT

# # memory_file = os.path.join(
# #     os.path.dirname(__file__),
# #     "memory.json",
# # )

# # chat_history_file = os.path.join(
# #     os.path.dirname(__file__),
# #     "chat_history.json",
# # )


# # class QueryEmbeddingService:
# #     @staticmethod
# #     def generate_query_embedding(query_text, client, model="text-embedding-ada-002"):
# #         """Generate an embedding vector for the given query text using the specified model."""

# #         try:
# #             response = client.embeddings.create(
# #                 input=[query_text],
# #                 model=model
# #             )
# #             if response.data and len(response.data) > 0:
# #                 return response.data[0].embedding
# #             else:
# #                 print("Warning: No embedding returned for the query.")
# #                 return None
# #         except Exception as e:
# #             return Response(
# #                 ERROR_RESPONSE_OBJECT,
# #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             )


# # class VectorSearchService:
# #     @staticmethod
# #     def perform_vector_search(query_embedding, collection, n_results=5):
# #         """Perform a vector similarity search in the collection based on the query embedding."""

# #         if query_embedding is None:
# #             return Response(
# #                 ERROR_RESPONSE_OBJECT,
# #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             )

# #         try:
# #             results = collection.query(
# #                 query_embeddings=[query_embedding],
# #                 n_results=n_results,
# #                 include=['documents'],
# #             )

# #             if results and results.get('documents') and results['documents'][0]:
# #                 return results['documents'][0]
# #             else:
# #                 print("No results found for the query.")
# #                 return []

# #         except Exception:
# #             return Response(
# #                 ERROR_RESPONSE_OBJECT,
# #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             )


# # class FileStorageService:
# #     @staticmethod
# #     def save_memory(key: str, value: str):
# #         """Store a key-value pair in memory file"""

# #         memory = {}

# #         if os.path.exists(memory_file):
# #             try:
# #                 with open(memory_file, "r") as f:
# #                     content = f.read().strip()
# #                     memory = json.loads(content)
                    
# #             except Exception as e:
# #                 memory = {}

# #         memory[key] = value

# #         try:
# #             with open(memory_file, "w") as f:
# #                 json.dump(memory, f, indent=2)
# #             return "Stored successfully"
        
# #         except Exception as e:
# #             return Response(
# #                 ERROR_RESPONSE_OBJECT,
# #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             )

# #     @staticmethod
# #     def load_memory(query: str):
# #         """Search for stored memories matching the query"""

# #         if not os.path.exists(memory_file):
# #             return "No memories stored"

# #         try:
# #             with open(memory_file, "r") as f:
# #                 content = f.read().strip()
# #                 if not content:
# #                     return "No memories stored"

# #                 memory = json.loads(content)
# #                 if not memory:
# #                     return "No memories stored"

# #                 return json.dumps(memory, indent=2)

# #         except json.JSONDecodeError:
# #             return Response(
# #                 ERROR_RESPONSE_OBJECT,
# #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             )
            
# #         except Exception:
# #             return Response(
# #                 ERROR_RESPONSE_OBJECT,
# #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             )

# #     @staticmethod
# #     def load_chat_history():
# #         """Load chat history from JSON file"""

# #         if os.path.exists(chat_history_file):
# #             try:
# #                 with open(chat_history_file, "r") as f:
# #                     return json.load(f)
                
# #             except (json.JSONDecodeError, IOError):
# #                 return []
            
# #         return []

# #     @staticmethod
# #     def save_chat_history(history):
# #         """Save chat history to JSON file."""

# #         try:
# #             with open(chat_history_file, "w") as f:
# #                 json.dump(history, f, indent=2)
                
# #         except Exception:
# #             return Response(
# #                 ERROR_RESPONSE_OBJECT,
# #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             )


# # class AIResponseService:
# #     @staticmethod
# #     def generate_ai_response(tools, system_message, query_text, search_results, client, model="gpt-4o-mini"):
# #         context = "\n\n".join(search_results) if search_results else ""
# #         user_message = (
# #             f"Based on the following context, answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
# #             if context
# #             else f"Based on the following context, and the result returned by the tool `recall_fact` answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
# #         )

# #         history = FileStorageService.load_chat_history()
# #         messages = [
# #             {"role": "system", "content": system_message},
# #             *history,
# #             {"role": "user", "content": user_message},
# #         ]

# #         try:
# #             # First API call - check for tool usage
# #             response = AIResponseService._chat_completion(
# #                 client, messages, model, tools, stream=False)

# #             collected_response = ""

# #             if response.choices[0].message.tool_calls:
# #                 messages.append(response.choices[0].message)

# #                 # Handle tool calls
# #                 for tool_call in response.choices[0].message.tool_calls:
# #                     args = {}
# #                     try:
# #                         if tool_call.function.arguments and tool_call.function.arguments.strip():
# #                             args = json.loads(tool_call.function.arguments)
# #                     except json.JSONDecodeError:
# #                         messages.append({
# #                             "role": "tool",
# #                             "tool_call_id": tool_call.id,
# #                             "content": "Error: Could not parse tool arguments"
# #                         })
# #                         continue

# #                     # Execute tools
# #                     result = None
# #                     if tool_call.function.name == "store_fact":
# #                         result = FileStorageService.save_memory(args.get("key"), args.get(
# #                             "value")) if "key" in args and "value" in args else "Error: Missing key or value"
# #                     elif tool_call.function.name == "recall_fact":
# #                         result = FileStorageService.load_memory(
# #                             args.get("query")) if "query" in args else "Error: Missing query"

# #                     if result:
# #                         messages.append({
# #                             "role": "tool",
# #                             "tool_call_id": tool_call.id,
# #                             "content": str(result)
# #                         })

# #                 # Second API call with tool results (streaming)
# #                 final_response = AIResponseService._chat_completion(
# #                     client, messages, model, stream=True)

# #             else:
# #                 # Direct response (streaming)
# #                 final_response = AIResponseService._chat_completion(
# #                     client, messages, model, stream=True)

# #             # Stream results
# #             for chunk in final_response:
# #                 delta = chunk.choices[0].delta
# #                 if delta and delta.content:
# #                     content = delta.content
# #                     collected_response += content
# #                     yield json.dumps({"chunk": content}) + "\n\n"

# #             yield json.dumps({"chunk": "[DONE]"}) + "\n\n"

# #             # Save history
# #             history.append({"role": "user", "content": query_text})
# #             history.append(
# #                 {"role": "assistant", "content": collected_response})
# #             FileStorageService.save_chat_history(history)

# #         except Exception as e:
# #             return None

# #     @staticmethod
# #     def generate_event_stream(ai_response):
# #         for chunk in ai_response:
# #             yield f"data: {chunk}"

# #     @staticmethod
# #     def _chat_completion(client, messages, model="gpt-4o-mini", tools=None, stream=False):
# #         """
# #         Helper to create a chat completion with common parameters.
# #         """

# #         params = {
# #             "model": model,
# #             "messages": messages,
# #             "temperature": 0.3,
# #             "frequency_penalty": 1.0,
# #             "presence_penalty": 1.0,
# #             "max_tokens": 100,
# #             "top_p": 0.3,
# #             "stream": stream,
# #         }

# #         if tools:
# #             params["tools"] = tools
# #             params["tool_choice"] = "auto"

# #         return client.chat.completions.create(**params)


import os
import json

from rest_framework.response import Response
from rest_framework import status

from src.chatbot.constants import ERROR_RESPONSE_OBJECT

memory_file = os.path.join(
    os.path.dirname(__file__),
    "memory.json",
)

chat_history_file = os.path.join(
    os.path.dirname(__file__),
    "chat_history.json",
)


class QueryEmbeddingService:
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
                return None

        except Exception:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VectorSearchService:
    @staticmethod
    def perform_vector_search(query_embedding, collection, n_results=5):
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
                return []

        except Exception:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FileStorageService:
    @staticmethod
    def save_memory(key: str, value: str):
        """Store a key-value pair in memory file"""

        memory = {}

        if os.path.exists(memory_file):
            try:
                with open(memory_file, "r") as f:
                    content = f.read().strip()
                    memory = json.loads(content)

            except Exception:
                memory = {}

        memory[key] = value

        try:
            with open(memory_file, "w") as f:
                json.dump(memory, f, indent=2)
            return "Stored successfully"

        except Exception:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def load_memory(query: str):
        """Search for stored memories matching the query"""

        if not os.path.exists(memory_file):
            return "No memories stored"

        try:
            with open(memory_file, "r") as f:
                content = f.read().strip()
                if not content:
                    return "No memories stored"

                memory = json.loads(content)
                if not memory:
                    return "No memories stored"

                return json.dumps(memory, indent=2)

        except json.JSONDecodeError:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def load_chat_history():
        """Load chat history from JSON file"""

        if os.path.exists(chat_history_file):
            try:
                with open(chat_history_file, "r") as f:
                    return json.load(f)

            except (json.JSONDecodeError, IOError):
                return []

        return []

    @staticmethod
    def save_chat_history(history):
        """Save chat history to JSON file"""

        try:
            with open(chat_history_file, "w") as f:
                json.dump(history, f, indent=2)

        except Exception:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AIResponseService:
    @staticmethod
    def generate_ai_response(tools, system_message, query_text, search_results, client, model="gpt-4o-mini"):
        context = "\n\n".join(search_results) if search_results else ""
        user_message = (
            f"Based on the following context, answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
            if context
            else f"Based on the following context, and the result returned by the tool `recall_fact` answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
        )

        history = FileStorageService.load_chat_history()
        messages = [
            {"role": "system", "content": system_message},
            *history,
            {"role": "user", "content": user_message},
        ]

        try:
            # First API call - check for tool usage
            response = AIResponseService._get_chat_completion(
                client, messages, model, tools, stream=False,
            )

            collected_response = ""

            if response.choices[0].message.tool_calls:
                messages.append(response.choices[0].message)

                # Handle tool calls
                for tool_call in response.choices[0].message.tool_calls:
                    args = {}
                    try:
                        if tool_call.function.arguments and tool_call.function.arguments.strip():
                            args = json.loads(tool_call.function.arguments)

                    except json.JSONDecodeError:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": "Error: Could not parse tool arguments"
                        })
                        continue

                    # Execute tools
                    result = None
                    if tool_call.function.name == "store_fact":
                        result = FileStorageService.save_memory(
                            args.get("key"), args.get("value")
                        ) if "key" in args and "value" in args else "Error: Missing key or value"

                    elif tool_call.function.name == "recall_fact":
                        result = FileStorageService.load_memory(
                            args.get("query")
                        ) if "query" in args else "Error: Missing query"

                    if result:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result)
                        })

                # Second API call with tool results (streaming)
                final_response = AIResponseService._get_chat_completion(
                    client, messages, model, stream=True,
                )

            else:
                # Direct response (streaming)
                final_response = AIResponseService._get_chat_completion(
                    client, messages, model, stream=True,
                )

            # Stream results
            for chunk in final_response:
                delta = chunk.choices[0].delta

                if delta and delta.content:
                    content = delta.content
                    collected_response += content

                    yield json.dumps({"chunk": content}) + "\n\n"

            yield json.dumps({"chunk": "[DONE]"}) + "\n\n"

            # Save history
            history.append(
                {"role": "user", "content": query_text}
            )
            history.append(
                {"role": "assistant", "content": collected_response}
            )
            FileStorageService.save_chat_history(history)

        except Exception:
            return None

    @staticmethod
    def generate_event_stream(ai_response):
        for chunk in ai_response:
            yield f"data: {chunk}"

    @staticmethod
    def _use_tools(messages, response):
        messages.append(response.choices[0].message)

        # Handle tool calls
        for tool_call in response.choices[0].message.tool_calls:
            args = {}
            try:
                if tool_call.function.arguments and tool_call.function.arguments.strip():
                    args = json.loads(tool_call.function.arguments)

            except json.JSONDecodeError:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": "Error: Could not parse tool arguments"
                })
                continue

            # Execute tools
            result = None
            if tool_call.function.name == "store_fact":
                result = FileStorageService.save_memory(
                    args.get("key"), args.get("value")
                ) if "key" in args and "value" in args else "Error: Missing key or value"

            elif tool_call.function.name == "recall_fact":
                result = FileStorageService.load_memory(
                    args.get("query")
                ) if "query" in args else "Error: Missing query"

            if result:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        return messages

    @staticmethod
    def _get_chat_completion(client, messages, model="gpt-4o-mini", tools=None, stream=False):
        """
        Helper to create a chat completion with common parameters.
        """

        params = {
            "model": model,
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0.3,
            "top_p": 0.3,
            "frequency_penalty": 1.0,
            "presence_penalty": 1.0,
            "stream": stream,
        }

        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"

        return client.chat.completions.create(**params)


## works

# import os
# import json

# import os
# import re

# from pdfminer.high_level import extract_text

# from rest_framework.response import Response
# from rest_framework import status

# from src.chatbot.adapters import ClientAdapter
# from src.chatbot.mixins import ContextProcessingMixin, FileStorageMixin

# from src.chatbot.config import SYSTEM_MESSAGE, TOOLS
# from src.chatbot.constants import ERROR_RESPONSE_OBJECT


# class ChatService(FileStorageMixin, ContextProcessingMixin):
#     def __init__(self):
#         super().__init__()

#         self.tools = TOOLS
#         self.system_message = SYSTEM_MESSAGE

#         self.memory_file = os.path.join(
#             os.path.dirname(__file__),
#             "memory.json",
#         )
#         self.chat_history_file = os.path.join(
#             os.path.dirname(__file__),
#             "chat_history.json",
#         )

#     def process_query(self, query):
#         """
#         Process user query using existing service logic
#         """
#         client = ClientAdapter.get_client()
#         collection = ClientAdapter.get_collection()
        
#         self.store_embeddings_and_chunks_into_db(client, collection)

#         try:
#             # Generate query embedding
#             query_embedding = self.generate_query_embedding(
#                 query,
#                 client,
#             )

#             if not query_embedding:
#                 return None

#             # Perform vector search
#             search_results = self.vector_search(
#                 query_embedding,
#                 collection,
#                 n_results=5,
#             )

#             ai_response = self._generate_ai_response(
#                 query,
#                 search_results,
#                 client,
#             )

#             for chunk in ai_response:
#                 yield f"data: {chunk}"

#         except Exception as e:
#             return Response(
#                 ERROR_RESPONSE_OBJECT,
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     def _generate_ai_response(self, query_text, search_results, client, model="gpt-4o-mini"):
#         context = "\n\n".join(search_results) if search_results else ""
#         user_message = (
#             f"Based on the following context, answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
#             if context
#             else f"Based on the following context, and the result returned by the tool `recall_fact` answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
#         )

#         history = self.load_chat_history()
#         messages = [
#             {"role": "system", "content": self.system_message},
#             *history,
#             {"role": "user", "content": user_message},
#         ]

#         try:
#             # First API call - check for tool usage
#             response = self._chat_completion(
#                 client, messages, model, stream=False, with_tools=True)

#             collected_response = ""

#             if response.choices[0].message.tool_calls:
#                 messages.append(response.choices[0].message)

#                 # Handle tool calls
#                 for tool_call in response.choices[0].message.tool_calls:
#                     args = {}
#                     try:
#                         if tool_call.function.arguments and tool_call.function.arguments.strip():
#                             args = json.loads(tool_call.function.arguments)
#                     except json.JSONDecodeError:
#                         messages.append({
#                             "role": "tool",
#                             "tool_call_id": tool_call.id,
#                             "content": "Error: Could not parse tool arguments"
#                         })
#                         continue

#                     # Execute tools
#                     result = None
#                     if tool_call.function.name == "store_fact":
#                         result = self.save_memory(args.get("key"), args.get(
#                             "value")) if "key" in args and "value" in args else "Error: Missing key or value"
#                     elif tool_call.function.name == "recall_fact":
#                         result = self.load_memory(
#                             args.get("query")) if "query" in args else "Error: Missing query"

#                     if result:
#                         messages.append({
#                             "role": "tool",
#                             "tool_call_id": tool_call.id,
#                             "content": str(result)
#                         })

#                 # Second API call with tool results (streaming)
#                 final_response = self._chat_completion(
#                     client, messages, model, stream=True)

#             else:
#                 # Direct response (streaming)
#                 final_response = self._chat_completion(
#                     client, messages, model, stream=True)

#             # Stream results
#             for chunk in final_response:
#                 delta = chunk.choices[0].delta
#                 if delta and delta.content:
#                     content = delta.content
#                     collected_response += content
#                     yield json.dumps({"chunk": content}) + "\n\n"

#             yield json.dumps({"chunk": "[DONE]"}) + "\n\n"

#             # Save history
#             history.append({"role": "user", "content": query_text})
#             history.append(
#                 {"role": "assistant", "content": collected_response})
#             self.save_chat_history(history)

#         except Exception:
#             return None

#     def _chat_completion(self, client, messages, model="gpt-4o-mini", stream=False, with_tools=False):
#         """
#         Helper to create a chat completion with common parameters.
#         """

#         params = {
#             "model": model,
#             "messages": messages,
#             "temperature": 0.3,
#             "frequency_penalty": 1.0,
#             "presence_penalty": 1.0,
#             "max_tokens": 100,
#             "top_p": 0.3,
#             "stream": stream,
#         }

#         if with_tools:
#             params["tools"] = self.tools
#             params["tool_choice"] = "auto"

#         return client.chat.completions.create(**params)
    
#     def store_embeddings_and_chunks_into_db(self, client, collection):
#         raw_text = self.load_pdf_text()
#         punctual_chunks = self.generate_chunks(
#             raw_text, chunk_size=600, overlap=100)
#         embeddings = self.generate_embeddings(punctual_chunks, client)

#         ids = [f"chunk_{i}" for i in range(len(embeddings))]
#         documents = list(embeddings.keys())
#         embedding_vectors = list(embeddings.values())

#         collection.add(
#             embeddings=embedding_vectors,
#             documents=documents,
#             ids=ids
#         )

#     @staticmethod
#     def generate_chunks(text, chunk_size=500, overlap=100):
#         split_points = r'(?<=[.!?;\n])\s*'
#         sentences = re.split(split_points, text)

#         chunks = []
#         current_chunk = ""
#         i = 0
#         while i < len(sentences):
#             sentence = sentences[i]

#             if len(current_chunk) + len(sentence) < chunk_size:
#                 current_chunk += sentence
#                 i += 1
#             else:
#                 if current_chunk:
#                     chunks.append(current_chunk.strip())
#                     overlap_start = max(0, len(current_chunk) - overlap)
#                     current_chunk = current_chunk[overlap_start:] + sentence
#                     i += 1
#                 else:
#                     chunks.append(sentence[:chunk_size].strip())
#                     sentences[i] = sentence[chunk_size:]
#                     if not sentences[i]:
#                         i += 1

#         if current_chunk:
#             chunks.append(current_chunk.strip())

#         return chunks

#     @staticmethod
#     def generate_embeddings(chunks, client, model="text-embedding-ada-002"):
#         chunk_embeddings = {}

#         try:
#             response = client.embeddings.create(
#                 input=chunks,
#                 model=model
#             )
#             for i, chunk in enumerate(chunks):
#                 if i < len(response.data):
#                     chunk_embeddings[chunk] = response.data[i].embedding
#                 else:
#                     print(f"Warning: No embedding returned for chunk {i+1}.")

#             return chunk_embeddings
#         except Exception as e:
#             print(f"An error occurred during embedding generation: {e}")
#             return None

#     @staticmethod
#     def load_pdf_text(filename="drf-react-gems.pdf"):
#         base_dir = os.path.dirname(os.path.abspath(__file__))
#         pdf_path = os.path.join(base_dir, "docs", filename)

#         return extract_text(pdf_path)

