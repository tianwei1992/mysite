from django.conf.urls import url
from .views import AboutView, CourseListView,HisCourseListView,ManageCourseListView, CreateCourseView, DeleteCourseView, UpdateCourseView,CreateLessonView

urlpatterns=[
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^course-list/$', CourseListView.as_view(), name="course_list"),
    url(r'^his-course-list/$', HisCourseListView.as_view(), name="his_course_list"),
    url(r'^manage-course/$', ManageCourseListView.as_view(), name="manage_course"),
    url(r'^create-course/$', CreateCourseView.as_view(), name="create_course"),
    url(r'^delete-course/(?P<pk>\d+)/$', DeleteCourseView.as_view(), name="delete_course"),
    url(r'^update-course/(?P<pk>\d+)/$', UpdateCourseView.as_view(), name="update_course"),
    url(r'^create-lesson/$', CreateLessonView.as_view(), name="create_lesson"),
]



