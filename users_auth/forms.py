
from django.forms import ModelForm
from django import forms

from users_auth.models import Users
from django.forms import ValidationError



class New_users(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email','password', 're_password','us_phone']
        def clean_email(self):
            email = self.cleaned_data.get('email')
            # check and raise error if other user already exists with given email
            is_exists = Users.objects.filter(email=email).exists()
            if is_exists:
                raise forms.ValidationError("User already exists with this email")
            return email
        def clean(self):
            form_data = self.cleaned_data
            if form_data['password'] != form_data['re_password']:
                self._errors["password"] = ["Password do not match"] # Will  a error message
                del form_data['password']
            return form_data
                

class User_Login(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Users
        fields = ['email','password']


class user_profile(ModelForm):
     password = forms.CharField(widget=forms.PasswordInput())
     class Meta:
        model = Users
        fields = ['first_name','last_name','email','password','us_phone','date_birth','faceboo_link','picture']           
