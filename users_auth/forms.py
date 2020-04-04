from django.forms import ModelForm
from django import forms

from users_auth.models import Users
from users_auth.global_var import *


class New_users(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password', 're_password', 'us_phone']


class User_Login(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['email', 'password']


class User_profile(ModelForm):
    # user = Users.objects.get(id=user_id)
    def __init__(self, *args, **kwargs):
        super(User_profile, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = Users
        fields = [ 'first_name', 'last_name', 'email', 'password', 'country', 'us_phone', 'date_birth',
                  'faceboo_link']
        date_birth = forms.DateField(
        widget=forms.DateInput(format='%m/%d/%Y'),
        input_formats=('%m/%d/%Y', )
        )


class DeleteAccount(ModelForm):
    class Meta:
        model = Users
        fields = ['password']

