from django.db import models
from django.core.validators import *

# Create your models here.
class Users(models.Model):
    first_name = models.CharField(null=False , max_length=50)
    last_name = models.CharField(null=False , max_length=50)
    email = models.EmailField(null=False,max_length=254)
    password = models.CharField(null=False, max_length=50)
    re_password = models.CharField(null=False, max_length=50)
    usertype=models.BooleanField(default=True)
    country=models.CharField(max_length=50,default="")
    us_phone=models.CharField(null=True,max_length=12)
    date_birth =models.DateField(null=True)
    faceboo_link= models.URLField(null=True)
    picture = models.ImageField(upload_to='users', blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    email_confirmed = models.BooleanField(default=False)
    



