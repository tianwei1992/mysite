from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^list-images/$', views.list_images, name='list_images'),
    url(r'^upload-images/$', views.upload_image, name='upload_image'),
    url(r'^del-images/$', views.del_image, name='del_image'),
    url(r'^images/$', views.falls_images, name='falls_images'),
]
