from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.generics import ListAPIView

from .serializers import CourseSerializer,LessonSerializer,PaymentSerializer
from .models import Course,User,Lesson
# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class PaymentListView(ListAPIView):
    serializer_class = PaymentSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        course = self.request.query_params.get('course')
        lesson = self.request.query_params.get('lesson')

        if course:
            queryset = queryset.filter(course_or_lesson=course)

        if lesson:
            queryset = queryset.filter(course_or_lesson=lesson)

        return queryset