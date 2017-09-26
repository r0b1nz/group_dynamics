# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import serializers
from django.http import HttpResponse

from django.shortcuts import render


# def signup(request):
#     print(request.method)
#     return HttpResponse("Hello, world. You're at the mobile app.")

from django.contrib.auth.models import User
from rest_framework.authtoken.management.commands.drf_create_token import UserModel
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from mobile.models import UserProfile

# UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(source='user.password')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    # def create(self, validated_data):
    #
    #     base_user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )
    #     base_user.set_password(validated_data['password'])
    #     base_user.save()
    #
    #     user = UserProfile.objects.create(
    #         user=base_user,
    #         gender=validated_data['gender'],
    #         imei=validated_data['imei'],
    #         bt_name=validated_data['bt_name']
    #     )
    #
    #     return user

    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'], validated_data['email'],
    #                                     validated_data['password'])
    #     return user

    class Meta:
        model = UserProfile
        fields = ('password', 'username', 'email', 'first_name', 'last_name', 'gender', 'imei', 'bt_name')


class Register(ModelViewSet):
    # model = UserProfile()
    permission_classes = [
        rest_framework.permissions.AllowAny
    ]
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    # def post(self, request):
    #     return Response({"status": "success", "response": "User Successfully Created"}, status=status.HTTP_201_CREATED)

    #     user = User.objects.create(
    #             username=request.data.get('email'),
    #             email=request.data.get('email'),
    #             first_name=request.data.get('firstName'),
    #             last_name=request.data.get('lastName')
    #         )
    # user.set_password(str(request.data.get('password')))
    # user.save()
