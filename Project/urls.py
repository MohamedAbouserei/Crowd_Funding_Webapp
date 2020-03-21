
from django.urls import path, include
from . import views
urlpatterns = [
        path('', views.index, name='index'),
        path('addproject', views.addproject, name='addproject'),
        


]
