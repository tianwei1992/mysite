import unittest

from django.test import Client, TestCase
from django.contrib.auth.models import User

from .models import Course, Lesson


class BrandTest(TestCase):
    def setUp(self):
        # create a test user
        user = User.objects.create(username='testuser', id=1)
        user.set_password('12345')
        user.save()

        # create a course
        course = Course.objects.create(title='couse1', id=3,overview='course1 overview', user_id=1)
        course.save()

        # create a lesson
        lesson = Lesson.objects.create(title='lesson1', description='lesson1 description', user_id=1, course_id=3, attach=None)
        lesson.save()

        # Every test needs a client.
        self.client = Client()
        self.is_login = self.client.login(username='testuser', password='12345')

    def test_details(self):
        self.assertEqual(self.is_login,True)

        # Issue a GET request.
        response = self.client.get('/course/course-list/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Issue a POST request.
        response = self.client.post('/course/lessons-list/3',{'course_id':3})
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Issue a GET request.
        response = self.client.get('/course/lesson-detail/1')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
