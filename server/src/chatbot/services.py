import os
import json

from rest_framework.response import Response
from rest_framework import status

from src.chatbot.adapters import ClientAdapter
from src.chatbot.mixins import ContextProcessingMixin, FileStorageMixin

from src.chatbot.config import SYSTEM_MESSAGE, TOOLS
from src.chatbot.constants import ERROR_RESPONSE_OBJECT


class ChatService(FileStorageMixin, ContextProcessingMixin):
    def __init__(self):
        super().__init__()

        self.tools = TOOLS
        self.system_message = SYSTEM_MESSAGE

        self.memory_file = os.path.join(
            os.path.dirname(__file__),
            "memory.json",
        )
        self.chat_history_file = os.path.join(
            os.path.dirname(__file__),
            "chat_history.json",
        )

    def process_query(self, query):
        """
        Process user query using existing service logic
        """
        client = ClientAdapter.get_client()
        collection = ClientAdapter.get_collection()

        try:
            # Generate query embedding
            query_embedding = self.generate_query_embedding(
                query,
                client,
            )

            if not query_embedding:
                return None

            # Perform vector search
            search_results = self.vector_search(
                query_embedding,
                collection,
                n_results=5,
            )

            if not search_results:
                search_results = []

            ai_response = self._generate_ai_response(
                query,
                search_results,
                client,
            )

            for chunk in ai_response:
                yield f"data: {chunk}"

        except Exception as e:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _generate_ai_response(self, query_text, search_results, client, model="gpt-4o-mini"):
        context = "\n\n".join(search_results) if search_results else ""
        user_message = (
            f"Based on the following context, answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
            if context
            else f"Based on the following context, and the result returned by the tool `recall_fact` answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
        )

        history = self.load_chat_history()
        messages = [
            {"role": "system", "content": self.system_message},
            *history,
            {"role": "user", "content": user_message},
        ]

        try:
            # First API call - check for tool usage
            response = self._chat_completion(
                client, messages, model, stream=False, with_tools=True)

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
                        result = self.save_memory(args.get("key"), args.get(
                            "value")) if "key" in args and "value" in args else "Error: Missing key or value"
                    elif tool_call.function.name == "recall_fact":
                        result = self.load_memory(
                            args.get("query")) if "query" in args else "Error: Missing query"

                    if result:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result)
                        })

                # Second API call with tool results (streaming)
                final_response = self._chat_completion(
                    client, messages, model, stream=True)

            else:
                # Direct response (streaming)
                final_response = self._chat_completion(
                    client, messages, model, stream=True)

            # Stream results
            for chunk in final_response:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    content = delta.content
                    collected_response += content
                    yield json.dumps({"chunk": content}) + "\n\n"

            yield json.dumps({"chunk": "[DONE]"}) + "\n\n"

            # Save history
            history.append({"role": "user", "content": query_text})
            history.append(
                {"role": "assistant", "content": collected_response})
            self.save_chat_history(history)

        except Exception:
            return None

    def _chat_completion(self, client, messages, model="gpt-4o-mini", stream=False, with_tools=False):
        """
        Helper to create a chat completion with common parameters.
        """

        params = {
            "model": model,
            "messages": messages,
            "temperature": 0.3,
            "frequency_penalty": 1.0,
            "presence_penalty": 1.0,
            "max_tokens": 100,
            "top_p": 0.3,
            "stream": stream,
        }

        if with_tools:
            params["tools"] = self.tools
            params["tool_choice"] = "auto"

        return client.chat.completions.create(**params)
