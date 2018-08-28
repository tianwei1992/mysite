from django.conf.urls import url
from account import views

"""patch request to corresponding function of view"""
app_name = "account"
urlpatterns = [
    url('^login/$', views.user_login, name="user_login"),
]
