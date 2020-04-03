import os
from django.shortcuts import render
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.db.models import *
from ajaxuploader.views import AjaxFileUploader
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.template.response import TemplateResponse
from django.contrib.postgres.search import SearchVector
from django.views.decorators.csrf import csrf_exempt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):

    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    rates = Project_User_Donation.objects.values(
        'prj_id').annotate(Sum('rate'))
    pics = Project_pics.objects.all()
    today = dateFormat(datetime.now())
    projects = Projects.objects.values().order_by("-updated_at")
    for project in projects:
        project["startdate"] = dateFormat(project["startdate"])
        project["enddate"] = dateFormat(project["enddate"])
        project["today"] = today
        for rate in rates:
            if rate["prj_id"] == project["id"]:
                project["flag"] = True
                break
            else:
                project["flag"] = False
    return render(request, 'Project/projects.html', {'projects': projects, "rates": rates, "pics": pics, "userID": request.session.get('0')})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categories(request):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True:
        return HttpResponseRedirect('/users_auth/login/')
    categories = Categories.objects.all()
    return render(request, 'users_auth/categories.html', {'categories': categories})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcategory(request):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        category = Categories.objects.create(
            title=request.POST.get("catName", ""))
        category.save()
    return categories(request)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addproject(request):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        details = ProjectForm(request.POST, user_id=request.session.get('0'))
        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            project = details.save(commit=False)
            project.user_id = request.session.get('0')
            # Finally write the changes into database
            project.save()

            # redirect it to some another page indicating data
            # was inserted successfully
            return HttpResponseRedirect('/project/')

        else:

            # Redirect back to the same page if the data
            # was invalid
            categories = Categories.objects.all()
            return render(request, "Project/add_project.html", {'form': details, 'categories': categories})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = ProjectForm(None)
        categories = Categories.objects.all()
        return render(request, 'Project/add_project.html', {'form': form, 'categories': categories})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def django_image_and_file_upload_ajax(request):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        form = ImageFileUploadForm(request.POST, request.FILES)
        if form.is_valid():

            tmp = Projects.objects.get(id=request.POST.get('prj_pic'))
            pic = request.FILES['picture']
            request.FILES['picture'].name = str(request.POST.get(
                'prj_pic'))+"_"+request.FILES['picture'].name
            prj = Project_pics(picture=request.FILES['picture'], prj_pic=tmp)
            prj.save("projects/"+str(request.POST.get('prj_pic')))
            # form.save()
            return JsonResponse({'error': False, 'message': "uploaded"})
        else:
            return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = ImageFileUploadForm()
        projects = Users.objects.filter(
            id=int(request.session.get('0')))[0].users.all()
        return render(request, 'Project/project_images.html', {'form': form, 'projects': projects})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def project(request, prj_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        project = Projects.objects.get(id=prj_id)
        project.Nor = project.Nor+1
        fullrate = project.rate+float(request.body)
        project.rate = fullrate
        project.save()
        overall = project.rate/project.Nor
        return JsonResponse({'error': False, 'message': str(overall)})
    else:
        rates = Project_User_Donation.objects.values(
            'prj_id').annotate(Sum('rate')).filter(prj_id=prj_id)
        if Projects.objects.get(id=prj_id):
            project = Projects.objects.get(id=prj_id)
            today = dateFormat(datetime.now())
            project.startdate = dateFormat(project.startdate)
            project.enddate = dateFormat(project.enddate)
            pics = project.oproject.all()
            comments = Project_comments.objects.filter(
                prj_comment=prj_id).order_by('updated_at').reverse()
            users = Users.objects.all()
            tags = project.tags.split(",")
            if tags:
                if len(tags) == 2:
                    similar = Projects.objects.filter(
                        Q(tags__contains=tags[0]) | Q(tags__contains=tags[1]))
                else:
                    similar = Projects.objects.filter(tags__contains=tags[0])
            likes = Project_User_Comment_Post.objects.filter(
                prj_id=prj_id, status=1).values('comment_id').annotate(Count('status'))
            dislikes = Project_User_Comment_Post.objects.filter(
                prj_id=prj_id, status=2).values('comment_id').annotate(Count('status'))
            reports = Project_User_Report.objects.filter(
                prj_id=prj_id, user_id=request.session.get('0'))

            if(project.Nor != 0):
                overall = project.rate/project.Nor
            else:
                overall = 0
            if rates:
                return render(request, 'Project/project.html', {'reports': reports, 'dislikes': dislikes, 'likes': likes, 'similar': similar, 'project': project, "pics": pics, "overall": overall, "rates": rates[0]['rate__sum'], "comments": comments, "users": users,"today" : today})
            else:
                return render(request, 'Project/project.html', {'reports': reports, 'dislikes': dislikes, 'likes': likes, 'similar': similar, 'project': project, "pics": pics, "overall": overall, "comments": comments, "users": users,"today" : today})
        else:
            return HttpResponseRedirect('/project/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcomment(request, prj_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        comment = Project_comments.objects.create(title=request.POST.get('title'), prj_comment=Projects.objects.get(
            id=prj_id), user=Users.objects.get(id=request.session.get('0')))
        comment.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addlike(request, prj_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        comment, created = Project_User_Comment_Post.objects.get_or_create(
            comment_id=request.POST.get('comment_id'), prj_id=prj_id, user_id=request.session.get('0'))
        if created:
            comment.status = 1
            comment.save()
        else:
            comment.status = 1
            comment.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adddislike(request, prj_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        comment, created = Project_User_Comment_Post.objects.get_or_create(
            comment_id=request.POST.get('comment_id'), prj_id=prj_id, user_id=request.session.get('0'))
        if created:
            comment.status = 2
            comment.save()
        else:
            comment.status = 2
            comment.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecomment(request, prj_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        Project_comments.objects.get(
            id=request.POST.get('comment_id')).delete()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def donate(request, prj_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        rates = Project_User_Donation.objects.values(
            'prj_id').annotate(Sum('rate')).filter(prj_id=prj_id)
        project = Projects.objects.get(id=prj_id)
        if rates:
            if not (rates[0]['rate__sum'] + int(request.POST.get('donation_amount'))) > project.totaltarget:
                donation = Project_User_Donation.objects.create(prj=Projects.objects.get(
                    id=prj_id), user=Users.objects.get(id=request.session.get('0')), rate=request.POST.get('donation_amount'))
                donation.save()
        else:
            donation = Project_User_Donation.objects.create(prj=Projects.objects.get(
                id=prj_id), user=Users.objects.get(id=request.session.get('0')), rate=request.POST.get('donation_amount'))
            donation.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addreport(request, prj_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        project, created = Project_User_Report.objects.get_or_create(
            prj_id=prj_id, user_id=request.session.get('0'))
        if created:
            project.reports = True
            project.save()
        else:
            project.reports = True
            project.save()
        return HttpResponseRedirect('/project/'+str(prj_id)+'/details')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteproject(request, prj_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        project = Projects.objects.get(id=prj_id)
        rates = Project_User_Donation.objects.values(
            'prj_id').annotate(Sum('rate')).filter(prj_id=prj_id)
        if rates:
            ratio = float(Project_User_Donation.objects.values('prj_id').annotate(
                Sum('rate')).filter(prj_id=prj_id)[0]['rate__sum'])/project.totaltarget * 100
            if ratio <= 25:
                project.delete()
        else:
            project.delete()
        return HttpResponseRedirect('/project/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    request.session[0] = False
    return HttpResponseRedirect('/users_auth/login/')


def person(request):
    try:
        # of course some filter here
        return {'person': Users.objects.filter(id=request.session.get('0'))[0]}
    except:
        return {}


def dateFormat(dateToFormat):
    myFormat = "%Y-%m-%d %H:%M:%S"
    dateToFormat = dateToFormat.strftime(myFormat)
    dateToFormat = datetime.strptime(dateToFormat, "%Y-%m-%d %H:%M:%S")
    return dateToFormat

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    projects = Projects.objects.all().order_by("-created_at")
    categories = Categories.objects.all().order_by("-created_at")

    categoriesContext = {
        "categories": [
        ]
    }
    for category in categories:
        categoriesContext["categories"].append({
            "id": category.id,
            "title": category.title,
        })

    context = {
        "projects": [
        ]
    }
    today = dateFormat(datetime.now())
    for project in projects:
        donations = 0
        rates = Project_User_Donation.objects.values(
            'prj_id').annotate(Sum('rate')).filter(prj_id=project.id)
        for k in rates:
            if k["rate__sum"]:
                donations = donations + k["rate__sum"]
            else:
                donations = 0
        if project.Nor != 0:
            context["projects"].append({
                "id": project.id,
                "title": project.title,
                "details": project.details,
                "totaltarget": project.totaltarget,
                "totalrate": round(float(project.rate/project.Nor), 1),
                "rates": donations,
                'startdate': dateFormat(project.startdate),
                'enddate': dateFormat(project.enddate),
                'featured': project.featured,
                'created_at': project.created_at,
                'user': project.user_id,
                'today' : today
            })
        else:
            context["projects"].append({
                "id": project.id,
                "title": project.title,
                "details": project.details,
                "totaltarget": project.totaltarget,
                "totalrate": float(0),
                "rates": donations,
                'startdate': dateFormat(project.startdate),
                'enddate': dateFormat(project.enddate),
                'featured': project.featured,
                'created_at': project.created_at,
                'user': project.user_id,
                'today' : today
            })
    # context["projects"] = sorted(
    #     context["projects"], key=lambda k: k['created_at'], reverse=True)
    featuredProjectsContext = {
        "projects": [
        ]
    }
    for project in context["projects"]:
        if project["featured"]:
            featuredProjectsContext["projects"].append({
                "id": project["id"],
                "title": project["title"],
                "details": project["details"],
                "totaltarget": project["totaltarget"],
                "totalrate": project["totalrate"],
                "rate": project["rates"],
                'startdate': project["startdate"],
                'enddate': project["enddate"],
                'featured':  project["featured"],
                'user': project["user"],
                'today' : project["today"]
            })
    index = 0
    featuredProjectsContextToSend = {
        "projects": [
        ]
    }
    for project in featuredProjectsContext["projects"]:
        featuredProjectsContextToSend["projects"].append({
            "id": project["id"],
            "title": project["title"],
            "details": project["details"],
            "totaltarget": project["totaltarget"],
            "totalrate": project["totalrate"],
            "rate": project["rate"],
            'startdate': project["startdate"],
            'enddate': project["enddate"],
            'featured':  project["featured"],
            'user': project["user"],
            'today' : project["today"]
        })
        if(index == 4):
            break
        index = index + 1

    updatedProjects = {
        "projects": [
        ]
    }
    index = 0
    for project in context["projects"]:
        updatedProjects["projects"].append({
            "id": project["id"],
            "title": project["title"],
            "details": project["details"],
            "totaltarget": project["totaltarget"],
            "totalrate": project["totalrate"],
            "rate": project["rates"],
            'startdate': project["startdate"],
            'enddate': project["enddate"],
            'featured':  project["featured"],
            'user': project["user"],
            'today' : project["today"]
        })
        if(index == 4):
            break
        index = index + 1
    context["projects"] = sorted(
        context["projects"], key=lambda k: k['totalrate'], reverse=True)

    contextToSend = {
        "projects": [
        ]
    }
    index = 0
    for project in context["projects"]:
        contextToSend["projects"].append({
            "id": project["id"],
            "title": project["title"],
            "details": project["details"],
            "totaltarget": project["totaltarget"],
            "totalrate": project["totalrate"],
            "rate": project["rates"],
            'featured':  project["featured"],
            'user': project["user"],
            'today' : project["today"]
        })
        if(index == 4):
            break
        index = index + 1
    return render(request, 'Project/home.html', {'projects': contextToSend["projects"], 'updatedProjects': updatedProjects["projects"], 'featuredP': featuredProjectsContextToSend["projects"], "categories": categoriesContext["categories"], "userID": request.session.get('0')})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def lisCategoryProjects(request, cat_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'GET':        
        projects = Projects.objects.all().order_by("-created_at")
        category = Categories.objects.get(id=cat_id)
        categoryTitle = category.title
        catContext = {
            "category": [
            ]
        }
        catContext["category"].append({"title": category.title})
        context = {
            "projects": [
            ]
        }
        today = dateFormat(datetime.now())
        for project in projects:
            donations = 0
            rates = Project_User_Donation.objects.values(
                'prj_id').annotate(Sum('rate')).filter(prj_id=project.id)
            for k in rates:
                if k["rate__sum"]:
                    donations = donations + k["rate__sum"]
                else:
                    donations = 0
            if project.cat_id == cat_id:
                if project.Nor != 0:
                    context["projects"].append({
                        "id": project.id,
                        "title": project.title,
                        "details": project.details,
                        "totaltarget": project.totaltarget,
                        "totalrate": round(float(project.rate/project.Nor), 1),
                        "rates": donations,
                        'startdate': dateFormat(project.startdate),
                        'enddate': dateFormat(project.enddate),
                        'featured': project.featured,
                        'created_at': project.created_at,
                        'user': project.user_id,
                        'today' : today
                    })
                else:
                    context["projects"].append({
                        "id": project.id,
                        "title": project.title,
                        "details": project.details,
                        "totaltarget": project.totaltarget,
                        "totalrate": float(0),
                        "rates": donations,
                        'startdate': dateFormat(project.startdate),
                        'enddate': dateFormat(project.enddate),
                        'featured': project.featured,
                        'created_at': project.created_at,
                        'user': project.user_id,
                        'today' : today
                    })
        return render(request, 'Project/catProjects.html', {"projects": context["projects"], "category": categoryTitle, "userID": request.session.get('0')})


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def django_search_ajax(request):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is False:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        projects = Projects.objects.all()
        result = {}
        starts_with = request.POST.get('suggestion').strip()
        if starts_with:
            for project in projects:
                if starts_with in project.tags or project.title:

                    result.update({project.id: str(project)})
        return JsonResponse({'error': False, 'message': result})
