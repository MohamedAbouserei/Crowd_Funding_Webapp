
from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
        path('', views.index, name='index'),
        path('addproject', views.addproject, name='addproject'),
        path('addproject/pic', views.django_image_and_file_upload_ajax)

        
]
