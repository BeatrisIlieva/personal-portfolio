import json
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.config import HUMAN_TEMPLATE, SYSTEM_TEMPLATE
from src.chatbot.servicescopy import RetrievalService


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

        for event in self.app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):

            content = event['model']['messages'].content

            if content:
                for ch in content:
                    yield f"data: {json.dumps({'chunk': ch})}\n\n"
                    # time.sleep(0.02)

        # Completion signal
        yield f"data: {json.dumps({'chunk': '[DONE]'})}\n\n"
