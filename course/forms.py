from django import forms
from .models import Course,Lesson

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields =("title", "overview")

class CreateLessonForm(forms.ModelForm):
    class Meta:
        model=Lesson
        fields =("course", "title", "vedio", "description", "attach")
    def __init__(self, user, *args, **kwargs):
        super(CreateLessonForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user)
