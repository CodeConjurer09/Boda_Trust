from django.urls import path
from .views import EmergencyAlertCreateView, EmergencyAlertListView

urlpatterns = [
    path('create/', EmergencyAlertCreateView.as_view(), name='create-emergency-alert'),
    path('alerts/', EmergencyAlertListView.as_view(), name='list-emergency-alerts'),
]