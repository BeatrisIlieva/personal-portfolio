import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse

from .serializers import ChatRequestSerializer
from .services.chat_service import ChatService
from .services.document_processing_service import DocumentProcessingService
from .services.database_service import DatabaseService

logger = logging.getLogger(__name__)


class ChatBotAPIView(APIView):
    """
    Main chatbot API endpoint that handles user queries and returns AI responses.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database_service = None
        self.document_service = None
        self.chat_service = None

    def _initialize_services(self):
        """Initialize services if not already done"""
        if not self.database_service:
            self.database_service = DatabaseService()
        if not self.document_service:
            self.document_service = DocumentProcessingService()
        if not self.chat_service:
            self.chat_service = ChatService()

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
            "error": "error message if any"
        }
        """
        try:
            # Initialize services
            self._initialize_services()

            # Validate input
            serializer = ChatRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'detail': 'Sorry, something went wrong. Please try again later.',
                    'success': False,
                    'error': 'Invalid input: ' + str(serializer.errors)
                }, status=status.HTTP_400_BAD_REQUEST)

            user_message = serializer.validated_data['message']
            logger.info(f"Received user query: {user_message}")

            response = StreamingHttpResponse(
                self._process_query(user_message),
                content_type='text/event-stream'
            )

            if not response:
                return Response({
                    'detail': 'Sorry, something went wrong. Please try again later.',
                    'success': False,
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            response['Cache-Control'] = 'no-cache'
            # Disable buffering in proxies like Nginx
            response['X-Accel-Buffering'] = 'no'
            return response

        except Exception as e:
            return Response({
                'detail': 'Sorry, something went wrong. Please try again later.',
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def _process_query(self, query):
        """
        Process user query using existing service logic
        """
        try:
            # Store embeddings
            self.document_service.store_embeddings_and_chunks_into_db()

            # Generate query embedding
            query_embedding = self.document_service.generate_query_embedding(
                query, self.database_service.client)

            if not query_embedding:
                return None

            # Perform vector search
            search_results = self.document_service.vector_search(
                query_embedding, self.database_service.collection, n_results=5)

            if not search_results:
                search_results = []

            for chunk in self.chat_service.generate_ai_response(
                query, search_results, self.database_service.client
            ):
                yield f"data: {chunk}"

        except Exception as e:
            return None
