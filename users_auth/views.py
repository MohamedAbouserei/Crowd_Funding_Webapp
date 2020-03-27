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


user_id=""

def home(request):
    return  render(request,'users_auth/home.html')



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

