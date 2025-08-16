from django.urls import path
from .views import RideRequestAPIView, RideListAPIView, RideStatusUpdateAPIView

urlpatterns = [
    path('request/', RideRequestAPIView.as_view(), name='ride_request'),
    path('', RideListAPIView.as_view(), name='ride_list'),
    path('<int:pk>/status/', RideStatusUpdateAPIView.as_view(), name='ride_status_update'),
]