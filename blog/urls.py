from django.conf.urls import url
from blog import views

urlpatterns = [
    url('^$', views.blog_title, name="blog_title"),
    url(r'(?P<article_id>\d)/$', views.blog_article, name="blog_detail"),
]
