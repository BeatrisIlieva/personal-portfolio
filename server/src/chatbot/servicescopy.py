# import json
# from langchain.prompts import ChatPromptTemplate
# from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# from src.chatbot.config import HUMAN_TEMPLATE, SYSTEM_TEMPLATE


# class RetrievalService:
#     """Handles document retrieval and context building."""

#     def __init__(self, vectorstore):
#         self.vectorstore = vectorstore

#     def get_context(self, query, k=4):
#         results = self.vectorstore.similarity_search(query, k=k)
#         for i, doc in enumerate(results, 1):
#             print(f"--- Chunk {i} ---")
#             print(doc.page_content, "...\n")
#         context = '\n'.join(result.page_content for result in results)

#         return context.strip()


# class ChatbotService:
#     """Core service for generating chatbot responses."""

#     def __init__(self, llm, vectorstore):
#         self.llm = llm
#         self.retrieval_service = RetrievalService(vectorstore)

#     def generate_response_stream(self, user_query, session_id, memory):

#         enhanced_query = self._create_enhanced_query(memory, user_query)

#         # Get context
#         context = self.retrieval_service.get_context(enhanced_query)

#         # Yield session_id first
#         yield f"data: {json.dumps({'session_id': session_id})}\n\n"

#         prompt = ChatPromptTemplate.from_messages([
#             SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
#             HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)
#         ])

#         # Get chat history
#         chat_history = memory.load_memory_variables({})['chat_history']

#         # Format messages
#         messages = prompt.format_messages(
#             chat_history=chat_history,
#             input=user_query,
#             context=context
#         )

        # # Stream response
        # full_response = ""
        # for chunk in self.llm.stream(messages):
        #     content = chunk.content
        #     if content:
        #         full_response += content
        #         yield f"data: {json.dumps({'chunk': content})}\n\n"

        # # Save to memory
        # memory.save_context({"input": user_query}, {"text": full_response})

        # # Completion signal
        # yield f"data: {json.dumps({'chunk': '[DONE]'})}\n\n"

#     def _create_enhanced_query(self, memory, user_query):
#         prompt = PromptTemplate(
#             input_variables=["conversation_memory", "user_query"],
#             template="""
#             Based on the conversation history and the user's current query, create a comprehensive search query for the vector database.

#             CONVERSATION HISTORY:
#             {conversation_memory}

#             CURRENT USER QUERY:
#             {user_query}

#             TASK: Combine context from the conversation with the current query to create a complete search query that captures:
#             1. Any product preferences mentioned earlier (category, metal, stone, color, collection, price range, size)
#             2. The specific request in the current query
#             3. Any constraints or requirements discussed previously
#             4. When you see from the conversation history that a product from a certain category has already been recommended, remove the category from the search query. Add a category that has not been recommended yet (all of the available categories are rings, earring, watch, bracelet and necklace). You are doing this because as customers are more likely to purchase a complete set—bracelet or watch, ring, necklace, and earrings—rather than multiples of the same type.
#             5. Take into consideration that:
#             - If a user says they are looking for an emerald, they mean a green stone.
#             - If a user says they are looking for a ruby, they mean a red stone.
#             - If a user says they are looking for an aquamarine, they mean an aquamarine-colored stone.
#             EXAMPLES:
#             - If user asked about "earrings under $3000" earlier and now says "do you have gold options?", expand to: "gold earrings under $3000"
#             - If the user mentions the word emerald, add green to the search query.
#             - Apply the same logic for ruby → red and aquamarine → aquamarine.

#             OUTPUT: Return only the enhanced search query - no explanations, no quotes, just the search terms.
#             """
#         )
#         chain = prompt | self.llm

#         inputs = {
#             "conversation_memory": memory,
#             "user_query": user_query
#         }

#         enhanced_query = chain.invoke(inputs)

#         print(enhanced_query.content)

#         return enhanced_query.content

#     def _check_if_matches_exist(self, query, context):
#         prompt = PromptTemplate(
#             input_variables=["query", "context"],
#             template="""
#             The context consists of chunks generated after a vector search on our product catalog:
#             {context}

#             The query consists of characteristic that a customer is looking for in a product in order to buy it:
#             {query}


#             Each product description is represented into the following example format:
#             `
#             Collection: Gerbera; Color: White; Metal: Yellow Gold; Stone: Diamond; Category: Earring; Product ID: 8;
#             Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746115898/21_o5ytzr.webp; Sizes: Size:
#             Small - Price: $1608.00,Size: Medium - Price: $1720.00,Size: Large - Price: $1828.00; Average Rating: 4.3/5
#             stars;
#             `
#             A product description starts with `Collection...` and ends with `stars;`.

#             You have to return one of these three possible conclusion:
#                 1. `The product is what the customer is looking for.`
#                 2. `The customer might be interested into the product.`
#                 3. `The product is not what the customer is looking for.`

#             If all of the words that the query contains of appear into a single product description, then your conclusion must be 1.
#             If some the words that the query contains of appear into a single product description, then your conclusion must be 2.
#             If none of the words that the query contains of appear into a single product description, then your conclusion must be 3.
#             """
#         )


import json
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.config import HUMAN_TEMPLATE, SYSTEM_TEMPLATE

import time


class RetrievalService:
    """Handles document retrieval and context building."""

    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def get_context(self, query, k=4):
        results = self.vectorstore.similarity_search(query, k=k)
        for i, doc in enumerate(results, 1):
            print(f"--- Chunk {i} ---")
            print(doc.page_content, "...\n")
        context = '\n'.join(result.page_content for result in results)

        return context.strip()


class ChatbotService:
    """Core service for generating chatbot responses."""

    def __init__(self, llm, vectorstore, app, memory):
        self.llm = llm
        self.retrieval_service = RetrievalService(vectorstore)
        self.app = app
        self.memory = memory

    def generate_response_stream(self, user_query, session_id):

        # Get context
        context = self.retrieval_service.get_context(user_query)
        # context = self.retrieval_service.get_context(enhanced_query)

        # Yield session_id first
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        config = {"configurable": {"thread_id": session_id}}

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)
        ])

        # Format messages
        messages = prompt.format_messages(
            chat_history=self.memory,
            input=user_query,
            context=context
        )

        system_message = messages[0]
        human_message = messages[1]

        for event in self.app.stream({"messages": [system_message, human_message]}, config, subgraphs=True, stream_mode="updates"):

            content = event['model']['messages'].content

            if content:
                for ch in content:
                    yield f"data: {json.dumps({'chunk': ch})}\n\n"
                    # time.sleep(0.02)

        # Completion signal
        yield f"data: {json.dumps({'chunk': '[DONE]'})}\n\n"
