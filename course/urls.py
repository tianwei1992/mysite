from django.conf.urls import url
from .views import AboutView, CourseListView

urlpatterns=[
    url(r'about/$', AboutView.as_view(), name="about"),
    url(r'course-list/$', CourseListView.as_view(), name="course_list"),
]



