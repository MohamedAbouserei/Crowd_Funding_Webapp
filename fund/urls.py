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
from django.contrib import admin
from django.urls import path, include
from users_auth import urls, views
from Project import urls
from django.conf import settings
from django.conf.urls.static import static
import Project

urlpatterns = [
    path('', Project.views.home),
    path('admin/', admin.site.urls),
    path('admins/addcategory/', views.addcategory, name='addcategory'),
    path('users_auth/', include('users_auth.urls')),
    path('project/', include('Project.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
