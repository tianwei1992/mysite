from django.conf.urls import url
from blog import views

urlpatterns = [
    url('^$', views.blog_title, name="blog_title"),
]
