from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm

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
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return HttpResponse("Successfully")
        else:
            return HttpResponse("Sorry, you can not register.")
    else:
        user_form = RegistrationForm()
        return render(request, "account/register.html", {"form": user_form})
