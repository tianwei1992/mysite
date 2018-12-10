from django.conf.urls import url
from .views import AboutView, CourseListView,HisCourseListView,ManageCourseListView, CreateCourseView, DeleteCourseView, UpdateCourseView,CreateLessonView,ListLessonView,DetailLessonView,DeleteLessonView, UpdateLessonView, StudentListLessonView,StudentDetailLessonView

urlpatterns=[
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^course-list/$', CourseListView.as_view(), name="course_list"),
    url(r'^his-course-list/$', HisCourseListView.as_view(), name="his_course_list"),
    url(r'^manage-course/$', ManageCourseListView.as_view(), name="manage_course"),
    url(r'^create-course/$', CreateCourseView.as_view(), name="create_course"),
    url(r'^delete-course/(?P<pk>\d+)/$', DeleteCourseView.as_view(), name="delete_course"),
    url(r'^update-course/(?P<pk>\d+)/$', UpdateCourseView.as_view(), name="update_course"),
    url(r'^create-lesson/$', CreateLessonView.as_view(), name="create_lesson"),
    url(r'^list-lessons/(?P<course_id>\d+)$', ListLessonView.as_view(), name="list_lessons"),
    url(r'^lessons-list/(?P<course_id>\d+)$', StudentListLessonView.as_view(), name="lessons_list"),
    url(r'^detail-lesson/(?P<lesson_id>\d+)$', DetailLessonView.as_view(), name="detail_lesson"),
    url(r'^lesson_detail/(?P<lesson_id>\d+)$',StudentDetailLessonView.as_view(), name="sdetail_lesson"),
    url(r'^delete-lesson/(?P<pk>\d+)/$', DeleteLessonView.as_view(), name="delete_lesson"),
    url(r'^update-lesson/(?P<pk>\d+)/$', UpdateLessonView.as_view(), name="update_lesson"),
]



