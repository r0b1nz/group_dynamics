import rest_framework
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from mobile.models import UserProfile


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'gender', 'imei', 'bt_name')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        base_user = User.objects.create(**user_data)
        account = UserProfile.objects.create(user=base_user, **validated_data)
        return account


class Register(ModelViewSet):
    permission_classes = [
        rest_framework.permissions.AllowAny
    ]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

