from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created')
    list_filter = ("user",)

# 注册的时候，将原模型和ModelAdmin耦合起来
admin.site.register(Course, CourseAdmin)
