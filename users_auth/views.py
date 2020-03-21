from django.shortcuts import render

from Project.models import *
from django.http import HttpResponse

def home(request):
    return  render(request,'users_auth/home.html')



def sign_up(request):
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
