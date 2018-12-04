from django.shortcuts import render
from .models import Course
from django.views.generic import TemplateView,ListView
from django.contrib.auth.models import User

class AboutView(TemplateView):
    template_name="course/about.html"

class CourseListView(ListView):
    model=Course
    context_object_name = "courses"
    template_name = "course/course_list.html"


class HisCourseListView(ListView):
    #queryset=Course.objects.filter(user__in=User.objects.filter(username="tester1"))
    model=Course
    def get_queryset(self):
        qs = super(HisCourseListView, self).get_queryset()
        return qs.filter(user=User.objects.filter(username="tester1")[0])
        # return qs.filter(user=User.objects.filter(username="tester1")[0])
    context_object_name = "courses"
    template_name = "course/course_list.html"
    
