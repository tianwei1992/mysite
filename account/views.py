from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserInfoForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, UserInfo

def user_login(request):
    if request.method == "POST":
        print(request.POST)
        login_form = LoginForm(request.POST)    # requests.POST(dict)
        if login_form.is_valid():
             cd = login_form.cleaned_data    # cd(dict)
             user = authenticate(username=cd["username"],password=cd["password"])    #return a User instance if match else None
             if user:
                 login(request, user)     # execute login
                 return HttpResponse("Login~Welcome~")
             else:
                 return HttpResponse("Fail!Check your username or password")
        else:
             return HttpResponse("Invalid data")
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})
            
def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid()* userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return render(request, 'account/register_success_done.html',)
        else:
            error_dict = {}
            error_dict.update(user_form.errors.as_data())
            error_dict.update(userprofile_form.errors.as_data())
            hints_dict = {"password" :"两次输入密码不一致",
                          "password2": "两次输入密码不一致",
                          "birth": "1900-01-01"}
            fields_convert_dict = {"password2":"密码", "birth":"生日"}
            error_message = '<br>'.join(["请检查["+ (fields_convert_dict.get(k) if fields_convert_dict.get(k) else k) + "], (提示:" + hints_dict.get(k) + ")" for k in error_dict])
            return HttpResponse("<strong>抱歉，注册没有成功o(╥﹏╥)o</strong> <br>{}".format(error_message))
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})

@login_required(login_url='/account/login/')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {"user":user, "userinfo":userinfo, "userprofile":userprofile})

@login_required(login_url='/account/login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    # origin:user=request.user,but does it matter?
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user) 

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid() and userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd['email'])
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
            return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth, "phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school,"company":userinfo.company,"address":userinfo.address, "aboutme":userinfo.aboutme,})
        return render(request, "account/myself_edit.html", {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form": userinfo_form, "userinfo": userinfo})


@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user = request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html',)


@login_required(login_url='/account/login/')
def my_messages(request):
    my_articles = request.user.article.all()
    my_comments = []
    [my_comments.extend(article.comments.all()) for article in my_articles]
    my_comments.sort(key=lambda t:t.created, reverse=True)

    applauds=[]
    [applauds.extend(article.applauds.all()) for article in my_articles]
    applauds.sort(key=lambda t:t.created, reverse=True)    

    return render(request, 'account/my_messages.html', {"comments":my_comments,"comments_cnt":len(my_comments), "applauds": applauds, "applauds_cnt":len(applauds)})

@login_required(login_url='/account/login/')
def password_change(request):
    if request.method == "POST":
        user_form = PasswordChangeForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(username=request.user.username, password=cd["old_password"])
            if user:
                user.set_password(cd['new_password2'])
                user.save()
                return render(request, 'account/password_change_done.html',)
            else:
                return render(request, "account/password_change_fail.html", {"mistake":"旧密码输入错误"})
        else:
            return render(request, "account/password_change_fail.html", {"mistake":"两次输入密码不一致"})
    else:
        # user_form = UserForm(instance=request.user)
        user_form = PasswordChangeForm()
        return render(request, "account/password_change_form.html", {"form":user_form})
