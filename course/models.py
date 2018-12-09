from django.db import models
from django.contrib.auth.models import User

from slugify import slugify
from .fields import OrderField

# Create your models here.

class Course(models.Model):
    user = models.ForeignKey(User, related_name='course_user', on_delete="CASCADE")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)

    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kargs)

    def __str__(self):
        return self.title

def user_directory_path(instance, filename):
    return "course/user_{}/{}".format(instance.user.id, filename)

class Lesson(models.Model):
    user = models.ForeignKey(User, related_name='lesson_user', on_delete="CASCADE")
    course = models.ForeignKey(Course, related_name='lesson', on_delete="CASCADE")
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to=user_directory_path)
    attach = models.FileField(upload_to=user_directory_path, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    order = OrderField(blank=True, for_fields=['course'])
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('order',)

    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super(Lesson, self).save(*args, **kargs)

    def __str__(self):
        return ('{}.{}'.format(self.order, self.title))

