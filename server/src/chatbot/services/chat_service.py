import os
import json


from src.chatbot.services.database_service import DatabaseService
from src.chatbot.config import SYSTEM_MESSAGE, TOOLS


MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")
CHAT_HISTORY = os.path.join(os.path.dirname(__file__), "chat_history.json")


class ChatService(DatabaseService):
    def __init__(self):
        super().__init__()
        super().__init__()
        self.tools = TOOLS

    def generate_ai_response(self, query_text, search_results, client, model="gpt-4o-mini"):
        """
        Generate AI response with memory capabilities and document context

        Args:
            query_text: User's question
            search_results: Results from ChromaDB search (list of strings)
            client: OpenAI client
            model: Model to use

        Returns:
            Generated response string or None if error
        """
        history = self._load_chat_history()

        # Handle both cases: with and without search results
        context = ""
        if search_results:
            context = "\n\n".join(search_results)

        # Create appropriate message based on whether we have context
        system_message = SYSTEM_MESSAGE

        if context:
            user_message = f"Based on the following context, answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"
        else:
            user_message = f"Based on the following context, and the result returned by the tool `recall_fact` answer the query:\n\nContext:\n{context}\n\nQuery: {query_text}"

        messages = [
            {"role": "system", "content": system_message},
            *history,
            {"role": "user", "content": user_message},
        ]

        try:
            # First API call - check for tool usage
            response = client.chat.completions.create(
                model=model,
                temperature=0.2,
                frequency_penalty=1.0,
                presence_penalty=1.0,
                messages=messages,
                max_tokens=100,
                top_p=0.2,
                tools=self.tools,
                tool_choice="auto",
            )

            collected_response = ""

            # Handle tool calls if any
            if response.choices[0].message.tool_calls:

                messages.append(response.choices[0].message)

                for tool_call in response.choices[0].message.tool_calls:
                    try:
                        # Handle empty or malformed arguments
                        if not tool_call.function.arguments or tool_call.function.arguments.strip() == "":
                            continue

                        args = json.loads(tool_call.function.arguments)

                    except json.JSONDecodeError as e:
                        # Add error message to maintain conversation flow
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": "Error: Could not parse tool arguments"
                        })
                        continue

                    # Execute the appropriate tool
                    result = None
                    try:
                        if tool_call.function.name == "store_fact":
                            if "key" in args and "value" in args:
                                result = self.save_memory(
                                    args["key"], args["value"])
                            else:
                                result = "Error: Missing key or value"

                        elif tool_call.function.name == "recall_fact":
                            if "query" in args:
                                result = self.load_memory(args["query"])
                            else:
                                result = "Error: Missing query"

                    except Exception as tool_error:
                        result = f"Tool execution error: {str(tool_error)}"

                    # Add tool result to conversation
                    if result:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result)
                        })

                # Second API call with tool results
                final_response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True
                )

                for chunk in final_response:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        content = delta.content
                        collected_response += content
                        yield json.dumps({"chunk": content}) + "\n\n"

            else:
                # No tool calls - stream direct response
                final_response = client.chat.completions.create(
                    model=model,
                    temperature=0.1,
                    messages=messages,
                    max_tokens=100,
                    top_p=0.1,
                    stream=True
                )

                for chunk in final_response:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        content = delta.content
                        collected_response += content
                        yield json.dumps({"chunk": content}) + "\n\n"

            yield json.dumps({"chunk": "[DONE]"}) + "\n\n"

            history.append({"role": "user", "content": query_text})
            history.append(
                {"role": "assistant", "content": collected_response})
            self._save_chat_history(history)

        except Exception as e:
            return None

    @staticmethod
    def save_memory(key: str, value: str):
        """Store a key-value pair in memory file with robust error handling"""
        memory = {}

        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    content = f.read().strip()
                    memory = json.loads(content)
            except Exception as e:
                memory = {}

        memory[key] = value

        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump(memory, f, indent=2)
            return "Stored successfully"
        except Exception as e:
            return f"Error storing memory: {e}"

    @staticmethod
    def load_memory(query: str):
        """Search for stored memories matching the query with robust error handling"""

        if not os.path.exists(MEMORY_FILE):
            return "No memories stored"

        try:
            with open(MEMORY_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return "No memories stored"

                memory = json.loads(content)
                if not memory:
                    return "No memories stored"

                return json.dumps(memory, indent=2)

        except json.JSONDecodeError as e:
            return "Memory file corrupted - please reset"
        except Exception as e:
            return f"Error reading memory: {e}"

    def _load_chat_history(self):
        """Load chat history from JSON file."""
        if os.path.exists(CHAT_HISTORY):
            try:
                with open(CHAT_HISTORY, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_chat_history(self, history):
        """Save chat history to JSON file."""
        try:
            with open(CHAT_HISTORY, "w") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error saving chat history: {e}")
