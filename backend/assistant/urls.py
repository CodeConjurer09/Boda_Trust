from django.urls import path
from .views import AssistantQueryCreateView, AssistantQueryListView

urlpatterns = [
    path('ask/', AssistantQueryCreateView.as_view(), name='assistant-ask'),
    path('queries/', AssistantQueryListView.as_view(), name='assistant-history'),
]