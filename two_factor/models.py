from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class TwoFactor(models.Model):
    number = models.CharField(max_length=16)
    user = models.OneToOneField(User)
