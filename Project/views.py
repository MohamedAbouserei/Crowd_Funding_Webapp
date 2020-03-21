from django.shortcuts import render
from Project.forms import ProjectForm

# Create your views here.
def index(request):
    
    return render(request, 'Project/contact.html')

def categories(request):
    
    categories = Categories.objects.all()
    return render(request, 'users_auth/categories.html',{'categories':categories})

def addcategory(request):
    if request.method == 'POST':
        category = Categories.objects.create(title=request.POST.get("catName", ""))
        category.save()
    return categories(request)

def addproject(request):
    if request.method == 'POST':
       details = ProjectForm(request.POST)
    return categories(request)