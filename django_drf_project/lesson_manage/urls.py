from django.urls import path
from rest_framework.routers import DefaultRouter

from lesson_manage.views import CourseViewSet, LessonListView, PaymentListView, LessonDetailView

router = DefaultRouter()

router.register(r'courses', CourseViewSet, basename='course')

app_name = 'lesson_manage'

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('payments/', PaymentListView.as_view(), name='payment'),
]

urlpatterns += router.urls
