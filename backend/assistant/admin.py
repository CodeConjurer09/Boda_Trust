from django.contrib import admin
from .models import AssistantQuery

@admin.register(AssistantQuery)
class AssistantQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query_text', 'created_at')
    search_fields = ('user__username', 'query_text')

