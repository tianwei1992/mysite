from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy
from account import views

"""patch request to corresponding function of view"""
app_name = "account"
urlpatterns = [
    # url('^login/$', views.user_login, name="user_login"),
    url(r'^login/$', auth_views.LoginView.as_view(), name="user_login"),
    url(r'^new-login/$', auth_views.LoginView.as_view(template_name="account/login.html"), name="user_login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="user_logout"),
    url(r'^new-logout/$', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="user_logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name="password_change"),
    url(r'^password-change-done/$', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    
    url(r'^new-password-change/$', auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html", success_url=reverse_lazy('account:password_change_done')), name="new_password_change"),
    url(r'^new-password-change-done/$', auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name="new_password_change_done"),
]
