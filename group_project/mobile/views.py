from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point, Polygon

from rest_framework import serializers, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import UserProfile, LocationDensity, GroupLocalization
from .constants import GEOFENCE_BOUNDS, UNKNOWN_GEOFENCE


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class UserProfileSerializer(ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'gender', 'imei', 'bt_name')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        base_user = User.objects.create_user(**user_data)
        account = UserProfile.objects.get_or_create(user=base_user, **validated_data)[0]
        return account


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserLoginSerializer(ModelSerializer):

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


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LocationDensitySerializer(ModelSerializer):
    class Meta:
        model = LocationDensity
        fields = '__all__'


class GroupLocalizationSerializer(ModelSerializer):
    class Meta:
        model = GroupLocalization
        fields = '__all__'


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def assign_groups(request):
    json = request.data
    if request.method == 'POST':
        username = json.keys()[0]
        data = json.values()[0]
        for entry in data:
            user = User.objects.get(username=username)
            timestamp = datetime.combine(
                datetime.strptime(entry['date'], '%d/%m/%Y').date(),
                datetime.strptime(entry['time'], '%H:%M').time()
            )
            GroupLocalization.objects.create(
                user=UserProfile.objects.get(user=user),
                timestamp=timestamp,
                group=str(entry['group'])
            )
            location = assign_geofence(entry['location']['lat'], entry['location']['long'])
            if LocationDensity.objects.filter(timestamp=timestamp, location=location).exists():
                loc_obj = LocationDensity.objects.get(timestamp=timestamp, location=location)
                loc_obj.density += 1
                loc_obj.save()
            else:
                LocationDensity.objects.create(timestamp=timestamp, location=location, density=1)
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Data format inaccurate !!!!!"})


def assign_geofence(lat, long):
    coordinates = Point(float(lat), float(long))
    for area in GEOFENCE_BOUNDS:
        points_list = [(point['lat'], point['long']) for point in GEOFENCE_BOUNDS[area]]
        points_list.append(points_list[0])
        polygon = Polygon(points_list)
        if polygon.contains(coordinates):
            return area
    return UNKNOWN_GEOFENCE
