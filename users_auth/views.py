from django.shortcuts import render

from users_auth.forms import *
from users_auth.models import Users

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from users_auth.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.shortcuts import render
from .forms import *
from Project.models import *
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.db.models import *


user_id = ""


def home(request):
    return render(request, 'users_auth/home.html')


def signup_new(request):
    if request.method == 'POST':
        form = New_users(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('users_auth/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return render(request, 'users_auth/acc_sent.html')
    else:
        form = New_users()
        return render(request, 'users_auth/sign_up.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = False
        user.save()
        #login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def thanks(request):
    user = Users.objects.all()
    return render(request, 'users_auth/success.html', {"user": user})


def user_login(request):
    global user_id
    form = User_Login()
    if request.method == 'POST':
        form = User_Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = Users.objects.filter(email=email, password=password)
            if user:
                # return HttpResponse("You are logged in your id is !")
                user_id = user[0].id
                request.session[0] = user[0].id
                if user[0].usertype == True:
                    return HttpResponseRedirect('/project/')
                else:
                    return HttpResponseRedirect('/users_auth/categories/')
            else:
                return render(request, "Project/login.html", {"form": form})

    else:
        return render(request, "Project/login.html", {"form": form})



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
def deletecategory(request, cat_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        category = Categories.objects.get(id=cat_id)
        category.delete()
    return HttpResponseRedirect('/users_auth/categories')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reports(request):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True:
        return HttpResponseRedirect('/users_auth/login/')
    reports = Project_User_Report.objects.all()
    return render(request, 'users_auth/reports.html', {'reports': reports})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletereportproject(request, rep_id):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        category = Projects.objects.get(id=rep_id)
        category.delete()
    return HttpResponseRedirect('/users_auth/reports')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def featuredProjects(request):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True:
        return HttpResponseRedirect('/users_auth/login/')
    projects = Projects.objects.all().order_by("-updated_at")
    context = {
        "projects": [
        ]
    }
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
                'startdate': project.startdate,
                'enddate': project.enddate,
                'featured': project.featured
            })
        else:
            context["projects"].append({
                "id": project.id,
                "title": project.title,
                "details": project.details,
                "totaltarget": project.totaltarget,
                "totalrate": float(0),
                "rates": donations,
                'startdate': project.startdate,
                'enddate': project.enddate,
                'featured': project.featured
            })
    return render(request, 'users_auth/featuredProjects.html',context=context)
def makeOrCancelFeature(request, projectId):
    if request.session.get('0', False) is False or Users.objects.filter(id=request.session.get('0'))[0].usertype is True:
        return HttpResponseRedirect('/users_auth/login/')
    if request.method == 'POST':
        project = Projects.objects.get(id=projectId)
        if project.featured:
            project.featured = False
        else:
            project.featured = True
        project.save()
    return HttpResponseRedirect('/users_auth/featuredProjects')
