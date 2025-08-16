from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import AssistantQuery
from .serializers import AssistantQuerySerializer
from .services import get_ai_response

class AssistantQueryCreateSet(generics.CreateAPIView):
    queryset = AssistantQuery.objects.all()
    serializer_class = AssistantQuerySerializer

    def perform_create(self, serializer):
        query_text = self.request.data.get('query_text')
        response_text = get_ai_response(query_text)
        serializer.save(user=self.request.user, response_text=response_text)

class AssistantQueryListView(generics.ListAPIView):
    serializer_class = AssistantQuerySerializer

    def get_queryset(self):
        return AssistantQuery.objects.filter(user=self.request.user).order_by('-created_at')