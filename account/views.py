from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

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
            

