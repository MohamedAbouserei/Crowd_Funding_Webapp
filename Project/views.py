import os
from django.shortcuts import render
from .forms import * 
from .models import *
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.db.models import *
from ajaxuploader.views import AjaxFileUploader
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
def index(request):
    rates=Project_User_Donation.objects.values('prj_id').annotate(Sum('rate'))
    pics=Project_pics.objects.all()
    projects=Projects.objects.all()
    return render(request, 'Project/projects.html',{'projects':projects,"rates":rates,"pics":pics})

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
            return render(request, "Project/add_project.html", {'form':details,'categories':categories})   
    else: 
  
        # If the request is a GET request then, 
        # create an empty form object and  
        # render it into the page 
        form = ProjectForm(None)
        categories = Categories.objects.all()    
        return render(request, 'Project/add_project.html', {'form':form,'categories':categories}) 

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
        return JsonResponse({'error': False, 'message':"uploaded"})
       else:
           return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = ImageFileUploadForm()
        return render(request, 'Project/project_images.html', {'form': form})
def project(request,prj_id):
    if request.method == 'POST':
        project = Projects.objects.get(id=prj_id)
        project.Nor=project.Nor+1
        fullrate=project.rate+float(request.body)
        project.rate=fullrate
        project.save()
        overall=project.rate/project.Nor
        return JsonResponse({'error': False, 'message':str(overall)})
    else:
        rates=Project_User_Donation.objects.values('prj_id').annotate(Sum('rate')).filter(prj_id=prj_id)
        if Projects.objects.get(id=prj_id):
            project = Projects.objects.get(id=prj_id)
        
            pics = project.oproject.all()
            comments=Project_comments.objects.filter(prj_comment=prj_id).order_by('updated_at').reverse()
            users=Users.objects.all()
            if(project.Nor!=0):
                overall=project.rate/project.Nor
            else:
                overall=0
            if rates :
                return render(request, 'Project/project.html', {'project': project,"pics":pics,"overall":overall,"rates":rates[0]['rate__sum'],"comments":comments,"users":users})
            else :
                return render(request, 'Project/project.html', {'project': project,"pics":pics,"overall":overall,"comments":comments,"users":users})
        else:
                    return HttpResponseRedirect('/project/')


def addcomment(request,prj_id):
    if request.method == 'POST':
        comment = Project_comments.objects.create(title=request.POST.get('title'),prj_comment=Projects.objects.get(id=prj_id),user=Users.objects.get(id=1)) 
        comment.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')
        
def addlike(request,prj_id):
    if request.method == 'POST':
        comment = Project_comments.objects.get(id=request.POST.get('comment_id'))
        comment.likes = comment.likes + 1
        comment.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')

def adddislike(request,prj_id):
    if request.method == 'POST':
        comment = Project_comments.objects.get(id=request.POST.get('comment_id'))
        comment.dislikes = comment.dislikes + 1
        comment.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')
    
def deletecomment(request,prj_id):
    if request.method == 'POST':
        Project_comments.objects.get(id=request.POST.get('comment_id')).delete()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')
    

def donate(request,prj_id):
    if request.method == 'POST':
        rates=Project_User_Donation.objects.values('prj_id').annotate(Sum('rate')).filter(prj_id=prj_id)
        project=Projects.objects.get(id=prj_id)
        if rates :
            if not (rates[0]['rate__sum'] + int(request.POST.get('donation_amount'))) > project.totaltarget :
                donation = Project_User_Donation.objects.create(prj=Projects.objects.get(id=prj_id),user=Users.objects.get(id=1),rate=request.POST.get('donation_amount')) 
                donation.save()
        else:
            donation = Project_User_Donation.objects.create(prj=Projects.objects.get(id=prj_id),user=Users.objects.get(id=1),rate=request.POST.get('donation_amount')) 
            donation.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')
    
def addreport(request,prj_id):
    if request.method == 'POST':
        project = Projects.objects.get(id=prj_id)
        project.reports = project.reports + 1
        project.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')

def deleteproject(request,prj_id):
    if request.method == 'POST':
        project=Projects.objects.get(id=prj_id)
        rates=Project_User_Donation.objects.values('prj_id').annotate(Sum('rate')).filter(prj_id=prj_id)
        if rates:
            ratio = float(Project_User_Donation.objects.values('prj_id').annotate(Sum('rate')).filter(prj_id=prj_id)[0]['rate__sum'])/project.totaltarget *100
            if ratio <= 25:
                project.delete()
        else: 
            project.delete()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')

    