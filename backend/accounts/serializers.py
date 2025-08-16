from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'is_driver', 'password', 'password2')

        def validate(self, attrs):
            if attrs['password'] != attrs['password']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            return attrs
        def create(self, validated_data):
            validated_data.pop('password2', None)
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
        
class UserSerializer(serializers.ModelSeriaizers):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'is_driver', 'is_verified', 'location')
        read_only_fields = ('is_verified',)