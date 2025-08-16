from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Ride
from .serializers import RideSerializer, RideStatusUpdateSerializer

class RideRequestAPIView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)

        
class RideListAPIView(generics.ListAPIView):
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_driver:
            return Ride.objects.filter(driver=user)
        return Ride.objects.filter(passenger=user)

class RideStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideStatusUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_update(self, serializer):
        ride = self.get_objects()
        if self.request.user != ride.driver:
            raise PermissionDenied("Only the assigned driver can update the ride status.")
        serializer.save()