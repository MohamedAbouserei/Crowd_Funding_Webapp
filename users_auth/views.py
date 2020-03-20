from django.shortcuts import render

from Project.models import *

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