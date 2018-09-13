from django.conf.urls import url
from account import views
from django.contrib.auth import views as auth_views
from django.urls import path

"""patch request to corresponding function of view"""
app_name = "account"
urlpatterns = [
    # url('^login/$', views.user_login, name="user_login"),
    url(r'^login/$', auth_views.LoginView.as_view(), name="user_login"),
    url(r'^new-login/$', auth_views.LoginView.as_view(template_name="account/login.html"), name="user_login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="user_logout"),
    url(r'^new-logout/$', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="user_logout"),
    url(r'^register/$', views.register, name="register"),
    
]
