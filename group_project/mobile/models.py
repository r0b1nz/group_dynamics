from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=6)
    imei = models.CharField(max_length=15, blank=True)
    bt_name = models.CharField(max_length=30, blank=True)
