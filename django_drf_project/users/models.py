from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(verbose_name='почта', unique=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/')

    # Add the other fields you want to use for the user

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    # Добавьте остальные поля пользователя, которые вы хотите использовать

class Course(models.Model):
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    course_or_lesson = models.CharField(max_length=200)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('transfer', 'Transfer')])

    def __str__(self):
        return f"Payment by {self.user} on {self.payment_date}"