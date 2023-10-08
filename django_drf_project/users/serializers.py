from rest_framework import serializers
from .models import Course,User,Lesson

class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_num_lessons(self, instance):
        return instance.lessons.count()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'