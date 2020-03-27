
from django.forms import ModelForm
from django import forms

from users_auth.models import Users


class New_users(ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email','password','us_phone']


class User_Login(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Users
        fields = ['email','password']
