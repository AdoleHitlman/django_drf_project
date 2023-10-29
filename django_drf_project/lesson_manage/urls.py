from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, PaymentListView, SubscriptionView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

app_name = 'lesson_manage'

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment'),
    path('subscribe/', SubscriptionView.as_view(), name='subscription'),

]

urlpatterns += router.urls