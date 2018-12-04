from django.conf.urls import url
from .views import AboutView, CourseListView,HisCourseListView,ManageCourseListView 

urlpatterns=[
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^course-list/$', CourseListView.as_view(), name="course_list"),
    url(r'^his-course-list/$', HisCourseListView.as_view(), name="his_course_list"),
    url(r'^manage-course/$', ManageCourseListView.as_view(), name="manage_course"),
]



