from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=6)
    imei = models.CharField(max_length=15, blank=True)
    bt_name = models.CharField(max_length=30, blank=True)


class LocationDensity(models.Model):
    timestamp = models.DateTimeField(unique=True)
    location = models.CharField(max_length=12)
    density = models.IntegerField(default=0)


class GroupLocalization(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    timestamp = models.TimeField()
    group = models.CharField(max_length=500)
