
from django.urls import path, include
from . import views
from django.conf.urls import url
from fund import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', views.index, name='index'),
        path('addproject', views.addproject, name='addproject'),
        path('addproject/pic', views.django_image_and_file_upload_ajax),
        path('<int:prj_id>/details/', views.project),

        
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
