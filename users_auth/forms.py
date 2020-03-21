
from django.forms import ModelForm

from users_auth.models import Users


class New_users(ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email','password','us_phone']