from rest_framework import serializers
from .models import AssistantQuery

class AssistantQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantQuery
        fields = '__all__'
        read_only_fields = ('response_text', 'created_at')
    