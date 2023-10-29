from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group

moderator_group, _ = Group.objects.get_or_create(name='Moderators')
users_group, _ = Group.objects.get_or_create(name='Users')
# Create your models here.
class User(AbstractUser):
    pass

