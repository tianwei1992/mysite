from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^article-column/$', views.article_column, name="article_column"),
    url(r'^rename-column/$', views.rename_article_column, name="rename_article_column"),
    url(r'^delete-column/$', views.delete_article_column, name="delete_article_column"),
    url(r'^article-post/$', views.article_post,name="article_post"),
]
