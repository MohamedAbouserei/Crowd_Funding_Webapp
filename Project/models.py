from django.db import models
from users_auth.models import Users
# Create your models here.

class Categories(models.Model):
    title = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Projects(models.Model):
    title = models.CharField(max_length=100,unique=True)
    details = models.TextField(null=True)
    totaltarget = models.IntegerField()
    rate = models.FloatField(default=0)
    Nor=models.IntegerField(default=0)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    tags = models.CharField(null=True,max_length=1000)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users')
    cat = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    def __id__(self):
        return self.id
    featured = models.BooleanField(default=False)

class Project_pics(models.Model):
    picture = models.ImageField()
    prj_pic = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='oproject')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Project_comments(models.Model):
    title = models.CharField(max_length=100,blank=False,default="----")
    prj_comment = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='cproject')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='cuser')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class comment_reply(models.Model):
    reply = models.CharField(max_length=100)
    comment = models.OneToOneField(Project_comments, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Project_User_Donation(models.Model):
    prj = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='dproject')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Project_User_Comment_Post(models.Model):
    prj = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='sproject')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='suser')
    comment = models.ForeignKey(Project_comments, on_delete=models.CASCADE, related_name='scomment')
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Project_User_Report(models.Model):
    prj = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='rproject')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='ruser')
    reports = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)








