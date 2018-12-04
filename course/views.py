from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name="course/about.html"
