import json
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from django.views.generic import TemplateView,ListView,CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateResponseMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from .forms import CreateCourseForm,CreateLessonForm
from .models import Course,Lesson

class AboutView(TemplateView):
    template_name="course/about.html"

class CourseListView(ListView):
    model=Course
    context_object_name = "courses"
    template_name = "course/course_list.html"


class UserMixin:
    """limit the queryset to the request.user only"""
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)
    
class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model=Course
    login_url = "/account/login/"

class UserLessonMixin(UserMixin, LoginRequiredMixin):
    model=Lesson
    login_url = "/account/login/"

class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = "course/manage/manage_course_list.html"

class HisCourseListView(ListView):
    def get_queryset(self):
        qs = super(HisCourseListView, self).get_queryset()
        return qs.filter(user=User.objects.filter(username="tester1")[0])
    model=Course
    context_object_name = "courses"
    template_name = "course/course_list.html"
    
class CreateCourseView(UserCourseMixin, CreateView):
    # context_object_name = "courses"
    template_name = "course/manage/create_course.html"
    fields =["title", "overview"]

    def post(self, request, *args, **kwargs):
        form=CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form":form})


class DeleteCourseView(UserCourseMixin, DeleteView):
#    template_name = "course/manage/delete_course.html"
     success_url = reverse_lazy("course:manage_course")
     def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result":"ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp

class UpdateCourseView(UserCourseMixin, UpdateView):
     template_name = "course/manage/update_course.html"
     success_url = reverse_lazy("course:manage_course")
     fields =["title", "overview"]

class CreateLessonView(LoginRequiredMixin, View):
    model = Lesson
    login_url = "/account/login/"
    
    def get(self, request, *args, **kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request, "course/manage/create_lesson.html", {"form":form})

    def post(self, request, *args, **kwargs):
        form = CreateLessonForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")
        else:
            return redirect("course:manage_course")
            


class ListLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/manage/list_lessons.html"

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return self.render_to_response({'course':course})
    
class DetailLessonView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        return self.render_to_response({'lesson':lesson})


class DeleteLessonView(UserLessonMixin, DeleteView):
#    template_name = "course/manage/delete_course.html"
     success_url = reverse_lazy("course:manage_course")

     def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.video.delete()
        self.object.attach.delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)

     def dispatch(self, *args, **kwargs):
        resp = super(DeleteLessonView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result":"ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp

class UpdateLessonView(UserLessonMixin, UpdateView):
     template_name = "course/manage/update_lesson.html"
     success_url = reverse_lazy("course:manage_course")
     fields =["title", "video", "attach"]

     def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)
