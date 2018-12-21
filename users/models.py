from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_site_admin = models.BooleanField(default=False)
