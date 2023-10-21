from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CourseSerializer,LessonSerializer,PaymentSerializer,MyTokenObtainPairSerializer
from .models import Course,Lesson
from .permissions import IsOwnerOrStaff
# Create your views here.



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    # Ваш код представления
    return Response({'message': 'Авторизовано!'})
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrStaff]
    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()
    def perform_update(self, serializer):
        cource = serializer.update

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrStaff]
    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
    def perform_update(self, serializer):
        lesson = serializer.update




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
