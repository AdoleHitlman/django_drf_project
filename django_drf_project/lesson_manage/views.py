from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Course, Lesson, Subscription
from .paginators import CoursePaginator, LessonPaginator
from .permissions import IsOwnerOrStaff
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrStaff]
    pagination_class = CoursePaginator

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        course = self.get_object()
        user = request.user

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        subscription.subscribed = True
        subscription.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        course = self.get_object()
        user = request.user

        Subscription.objects.filter(user=user, course=course).delete()

        return Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()


class LessonListView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrStaff]
    pagination_class = LessonPaginator

    def perform_create(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        lesson = serializer.save()


class PaymentListView(ListAPIView):
    serializer_class = PaymentSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        course = self.request.query_params.get('course')
        lesson = self.request.query_params.get('lesson')

        if course:
            # Для фильтрации по курсу, добавляем условие на поле "course"
            queryset = queryset.filter(course=course)

        if lesson:
            # Для фильтрации по уроку, добавляем условие на поле "lesson"
            queryset = queryset.filter(lesson=lesson)

        return queryset
