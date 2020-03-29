"""fund URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views
urlpatterns = [
	path('home/',views.home ,name='home'),
    path('sign_up/', views.signup_new ,name='sing-up'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
	path('success/', views.thanks, name='success'),
    path('login/', views.user_login, name='login'),
    path('categories/', views.categories, name='categories'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('<int:cat_id>/deletecategory/', views.deletecategory, name='deletecategory'),
    path('reports/', views.reports, name='reports'),
    path('<int:rep_id>/deletereportproject/', views.deletereportproject, name='deleteproject'),




]
