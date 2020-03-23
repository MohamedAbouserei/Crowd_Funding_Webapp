import os
from django.shortcuts import render
from .forms import * 
from .models import *
from django.http import JsonResponse
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage

from ajaxuploader.views import AjaxFileUploader
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
def index(request):
    

    return render(request, 'Project/test.html')

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

def django_image_and_file_upload_ajax(request):
    if request.method == 'POST':
       form = ImageFileUploadForm(request.POST, request.FILES)
       if form.is_valid():
        #myfile = request.FILES['picture']
        #fs = FileSystemStorage(location='D:/ITI/python/Project/fund/media/'+str(prj_id))
        #filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        tmp=Projects.objects.get(id=request.POST.get('prj_pic'))
        pic=request.FILES['picture']
        request.FILES['picture'].name = str(request.POST.get('prj_pic'))+"_"+request.FILES['picture'].name
        prj=Project_pics(picture=request.FILES['picture'],prj_pic=tmp)
        prj.save("projects/"+str(request.POST.get('prj_pic')))
        #form.save()
        return JsonResponse({'error': False, 'message':str(request.FILES['picture'])})
       else:
           return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = ImageFileUploadForm()
        return render(request, 'Project/test.html', {'form': form})