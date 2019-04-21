from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy
from account import views

"""patch request to corresponding function of view"""
app_name = "account"
urlpatterns = [
    # url('^login/$', views.user_login, name="user_login"),
    # url(r'^login/$', auth_views.LoginView.as_view(), name="user_login"),
    url(r'^new-login/$', auth_views.LoginView.as_view(template_name="account/login.html", redirect_authenticated_user=True), name="user_login"),
    # url(r'^logout/$', auth_views.LogoutView.as_view(), name="user_logout"),
    url(r'^new-logout/$', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="user_logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name="password_change"),
    url(r'^password-change-done/$', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    
    url(r'^new-password-change/$', views.password_change, name="new_password_change"),
    url(r'^new-password-change-done/$', auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name="new_password_change_done"),

    url(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html", success_url=reverse_lazy('account:password_reset_done'),email_template_name = 'account/password_reset_email.html',subject_template_name = 'account/password_reset_subject.txt'), name="password_reset"),
    url(r'^password-reset-done/$', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name="password_reset_done"),
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html", success_url=reverse_lazy('account:password_reset_complete')), name="password_reset_confirm"),
    url(r'^password-reset-complete/$', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name="password_reset_complete"),
    url(r'^my-information/$', views.myself, name="my_information"),
    url(r'^edit-my-information/$', views.myself_edit, name="edit_my_information"),
    url(r'my-image/$', views.my_image, name="my_image"),
    url(r'my-messages/$', views.my_messages, name="my_messages"),
]
