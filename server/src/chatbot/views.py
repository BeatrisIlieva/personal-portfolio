from django.http import StreamingHttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.chatbot.services import ChatService
from src.chatbot.serializers import ChatRequestSerializer

from src.chatbot.constants import ERROR_RESPONSE_OBJECT


class ChatBotAPIView(APIView, ChatService):
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

            response = StreamingHttpResponse(
                self.process_query(user_message),
                content_type='text/event-stream'
            )

            if not response:
                return Response(
                    ERROR_RESPONSE_OBJECT,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response['Cache-Control'] = 'no-cache'
            # Disable buffering in proxies like Nginx
            response['X-Accel-Buffering'] = 'no'

            return response

        except Exception as e:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
