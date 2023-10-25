from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson


class CourseTests(APITestCase):
    def test_create_course(self):
        url = reverse('course-list')
        data = {'title': 'Python Course', 'description': 'Learn Python programming'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_course(self):
        course = Course.objects.create(title='Python Course', description='Learn Python programming')
        url = reverse('course-detail', args=[course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course(self):
        course = Course.objects.create(title='Python Course', description='Learn Python programming')
        url = reverse('course-detail', args=[course.pk])
        data = {'title': 'Updated Python Course'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.title, 'Updated Python Course')

    def test_delete_course(self):
        course = Course.objects.create(title='Python Course', description='Learn Python programming')
        url = reverse('course-detail', args=[course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonTests(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(title='Python Course', description='Learn Python programming')

    def test_create_lesson(self):
        url = reverse('lesson-list')
        data = {'title': 'Introduction to Python', 'content': 'This is a lesson about Python'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lesson = Lesson.objects.get(pk=response.data['id'])
        self.assertEqual(lesson.course, self.course)

    def test_retrieve_lesson(self):
        lesson = Lesson.objects.create(course=self.course, title='Introduction to Python',
                                       content='This is a lesson about Python')
        url = reverse('lesson-detail', args=[lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(course=self.course, title='Introduction to Python',
                                       content='This is a lesson about Python')
        url = reverse('lesson-detail', args=[lesson.pk])
        data = {'title': 'Updated Introduction to Python'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'Updated Introduction to Python')

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(course=self.course, title='Introduction to Python',
                                       content='This is a lesson about Python')
        url = reverse('lesson-detail', args=[lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(title='Python Course', description='Learn Python programming')

    def test_subscribe_to_course(self):
        url = reverse('course-subscribe', args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['course'], self.course.pk)
        self.assertEqual(response.data['user'], self.client.user.pk)

    def test_unsubscribe_from_course(self):
        url = reverse('course-unsubscribe', args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.course.subscriptions.filter(user=self.client.user).exists())
