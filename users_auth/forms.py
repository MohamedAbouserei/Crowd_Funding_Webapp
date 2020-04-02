
from django.forms import ModelForm
from django import forms

from users_auth.models import Users
from users_auth.global_var  import *




class New_users(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email','password', 're_password','us_phone']
    
   
                

class User_Login(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Users
        fields = ['email','password']


class User_profile(ModelForm):
    # user = Users.objects.get(id=user_id)
    class Meta:
        model = Users
        fields = ['picture','first_name','last_name','email','password','us_phone','date_birth','faceboo_link']    
      
    # def __init__(self, *args, **kwargs):
    #     self.instance= kwargs.pop('instance')
    #     super(User_profile, self).__init__(*args, **kwargs)
    #     self.fields['first_name'].initial =instance.first_name
    #     self.fields['last_name'].initial = user["last_name"]
    #     self.fields['email'].initial = user["email"]
    #     self.fields['password'].initial = user["password"]

class DeleteAccount(ModelForm):
     class Meta:
        model = Users
        fields = ['password']