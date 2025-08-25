from django.http import StreamingHttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from src.chatbot.adapters import ClientAdapter
from src.chatbot.serializers import ChatRequestSerializer
from src.chatbot.services import AIResponseService, QueryEmbeddingService, VectorSearchService

from src.chatbot.constants import ERROR_RESPONSE_OBJECT
from src.chatbot.config import SYSTEM_MESSAGE, TOOLS


class ChatBotAPIView(APIView):
    """
    Main chatbot API endpoint that handles user queries and returns AI responses.
    """

    def post(self, request):
        """
        Handle POST requests for chatbot interactions

        Expected payload:
        {
            "message": "User's question"
        }

        Returns:
        {
            "response": "AI response",
            "success": true/false,
        }
        """
        try:
            # Validate input
            serializer = ChatRequestSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(
                    ERROR_RESPONSE_OBJECT,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_message = serializer.validated_data['message']

            ai_response = self._get_ai_response(user_message)

            streaming_response = StreamingHttpResponse(
                AIResponseService.generate_event_stream(ai_response),
                content_type='text/event-stream'
            )

            if not streaming_response:
                return Response(
                    ERROR_RESPONSE_OBJECT,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            streaming_response['Cache-Control'] = 'no-cache'
            # Disable buffering in proxies like Nginx
            streaming_response['X-Accel-Buffering'] = 'no'

            return streaming_response

        except Exception:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _get_ai_response(self, user_message):
        client = ClientAdapter.get_client()
        collection = ClientAdapter.get_collection()

        query_embedding = QueryEmbeddingService.generate_query_embedding(
            user_message,
            client,
        )

        if not query_embedding:
            return None

        search_results = VectorSearchService.perform_vector_search(
            query_embedding,
            collection,
        )

        ai_response = AIResponseService.generate_ai_response(
            TOOLS,
            SYSTEM_MESSAGE,
            user_message,
            search_results,
            client,
        )

        return ai_response
