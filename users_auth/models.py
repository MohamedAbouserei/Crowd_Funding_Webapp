from django.db import models

# Create your models here.
class Users(models.Model):
    first_name = models.CharField(null=False , max_length=50)
    last_name = models.CharField(null=False , max_length=50)
    email = models.EmailField(null=False,max_length=254)
    password = models.CharField(null=False, max_length=50)
    us_phone=models.CharField(null=True,max_length=12)
    date_birth =models.DateField(null=True)
    faceboo_link= models.URLField(null=True)
    picture = models.FileField(null=True,upload_to='pic_images/')
    created_date = models.DateField(auto_now_add=True)
    last_edit_date = models.DateField(auto_now=True)


