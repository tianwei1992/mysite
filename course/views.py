from django.shortcuts import render
from .models import Course
from django.views.generic import TemplateView,ListView

class AboutView(TemplateView):
    template_name="course/about.html"

class CourseListView(ListView):
    model=Course
    context_object_name = "courses"
    template_name = "course/course_list.html"
    
