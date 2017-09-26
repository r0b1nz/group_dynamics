# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=6)
    # username = models.CharField(max_length=30, unique=True)
    imei = models.CharField(max_length=15, blank=True)
    bt_name = models.CharField(max_length=30, blank=True)
