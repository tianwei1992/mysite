from django import forms

class LoginForm(forms.Form):
     username = forms.CharField()
     password = forms.CharField(widget=forms.PasswordInput)    #widget:specially set the HTML type
