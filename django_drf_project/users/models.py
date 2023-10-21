from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import Group
from django_drf_project import settings
moderator_group, _ = Group.objects.get_or_create(name='Moderators')
# Create your models here.
class User(AbstractUser):
    pass

# Добавьте остальные поля пользователя, которые вы хотите использовать

class Course(models.Model):
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    course_or_lesson = models.CharField(max_length=200)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('transfer', 'Transfer')])

    def __str__(self):
        return f"Payment by {self.user} on {self.payment_date}"
