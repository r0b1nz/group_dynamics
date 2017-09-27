import rest_framework
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from mobile.models import UserProfile


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class UserLoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        required=False, style={'input_type': 'password'}
    )

    default_error_messages = {
        'invalid_credentials': 'Unable to login with provided credentials.',
        'inactive_account': 'User account is disabled.',
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField(
            required=False
        )

    def validate(self, data):
        self.user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        #
        self._validate_user_exists(self.user)
        self._validate_user_is_active(self.user)
        return data

    def _validate_user_exists(self, user):
        if not user:
            self.fail('invalid_credentials')

    def _validate_user_is_active(self, user):
        if not user.is_active:
            self.fail('inactive_account')

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'gender', 'imei', 'bt_name')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        print(user_data)
        base_user = User.objects.create_user(**user_data)
        account = UserProfile.objects.get_or_create(user=base_user, **validated_data)[0]
        return account


class Register(ModelViewSet):
    permission_classes = [
        rest_framework.permissions.AllowAny
    ]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



