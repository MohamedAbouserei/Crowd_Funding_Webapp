from django.shortcuts import render

from .forms import *

from Project.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control


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
                if user[0].usertype == True:
                    return HttpResponseRedirect('/project/')
                else : 
                    return HttpResponseRedirect('/users_auth/categories/')
            else:
                 return render(request,"Project/login.html",{"form": form})

    else:
         return render(request,"Project/login.html",{"form": form})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categories(request):
  if request.session.get('0',False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True :return HttpResponseRedirect('/users_auth/login/')
  categories = Categories.objects.all()
  return render(request, 'users_auth/categories.html',{'categories':categories})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcategory(request):
    if request.session.get('0',False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True :return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        category = Categories.objects.create(title=request.POST.get("catName", ""))
        category.save()
    return categories(request)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecategory(request,cat_id):
    if request.session.get('0',False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True :return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        category = Categories.objects.get(id=cat_id)
        category.delete()
    return HttpResponseRedirect('/users_auth/categories')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reports(request):
    if request.session.get('0',False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True :return HttpResponseRedirect('/users_auth/login/')
    reports = Project_User_Report.objects.all()
    return render(request, 'users_auth/reports.html',{'reports':reports})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletereportproject(request,rep_id):
    if request.session.get('0',False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True :return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        category = Projects.objects.get(id=rep_id)
        category.delete()
    return HttpResponseRedirect('/users_auth/reports')