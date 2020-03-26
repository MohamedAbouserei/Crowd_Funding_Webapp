from django.shortcuts import render

from .forms import *

from Project.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect


user_id=""

def home(request):
    return  render(request,'users_auth/home.html')



def sign_up(request):
    form = New_users()
    if request.method == "POST":
        form = New_users(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users_auth/success.html', {"user": form })

    else:
        form = New_users()
    return render(request, 'users_auth/sign_up.html', {'form': form})


def thanks(request):
    user=Users.objects.all()
    return render(request,'users_auth/success.html',{"user": user })

def user_login(request):
    global user_id
    form=User_Login()
    if request.method == 'POST':
        form=User_Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user=Users.objects.filter(email=email,password=password)
            if user:
                #return HttpResponse("You are logged in your id is !")
                user_id=user[0].id
                request.session[0]=user[0].id
                title="you are logged in using %s%s" %(user[0].first_name,user[0].last_name)
                return HttpResponseRedirect('/project/')
            else:
                 return render(request,"Project/login.html",{"form": form})

    else:
         return render(request,"Project/login.html",{"form": form})




# Create your views here.
def index(request):
    
    return render(request, 'users_auth/index.html')

def categories(request):
    categories = Categories.objects.all()
    return render(request, 'users_auth/categories.html',{'categories':categories})

def addcategory(request):
    if request.method == 'POST':
        category = Categories.objects.create(title=request.POST.get("catName", ""))
        category.save()
    return categories(request)

