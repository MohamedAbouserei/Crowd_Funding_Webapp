from django.shortcuts import render
from .forms import ProjectForm 
from .models import *
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
       if details.is_valid():   
  
            # Temporarily make an object to be add some 
            # logic into the data if there is such a need 
            # before writing to the database    
            project = details.save(commit = False) 
  
            # Finally write the changes into database 
            project.save()   
  
            # redirect it to some another page indicating data 
            # was inserted successfully 
            return HttpResponse("data submitted successfully") 
              
       else: 
          
            # Redirect back to the same page if the data 
            # was invalid 
            categories = Categories.objects.all()    
            return render(request, "Project/contact.html", {'form':details,'categories':categories})   
    else: 
  
        # If the request is a GET request then, 
        # create an empty form object and  
        # render it into the page 
        form = ProjectForm(None)
        categories = Categories.objects.all()    
        return render(request, 'Project/contact.html', {'form':form,'categories':categories}) 
    