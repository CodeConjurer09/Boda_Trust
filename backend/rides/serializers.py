from rest_framework import serializers
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ('passenger', 'status', 'created_at', 'updated_at')
    

class RideStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride 
        fields = ('status',)