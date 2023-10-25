from rest_framework import serializers
from .models import Course, Lesson, Payment
from .validators import DescriptionValidator


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [DescriptionValidator(field='description')]

    def get_num_lessons(self, instance):
        return instance.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [DescriptionValidator(field='description')]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
