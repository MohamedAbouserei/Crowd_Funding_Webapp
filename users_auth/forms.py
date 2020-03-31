
from django.forms import ModelForm
from django import forms

from users_auth.models import Users
from django.forms import ValidationError



class New_users(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(New_users, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['re_password'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['us_phone'].widget.attrs['placeholder'] = 'Phone'

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email','password', 're_password','us_phone']


        


                

class User_Login(ModelForm):
    def __init__(self, *args, **kwargs):
            super(User_Login, self).__init__(*args, **kwargs)
    
            self.fields['email'].widget.attrs['placeholder'] = 'Email'
            self.fields['password'].widget.attrs['placeholder'] = 'Password'


    class Meta:
        model = Users
        fields = ['email','password']


class user_profile(ModelForm):
     class Meta:
        model = Users
        fields = ['first_name','last_name','email','password','us_phone','date_birth','faceboo_link','picture']           
