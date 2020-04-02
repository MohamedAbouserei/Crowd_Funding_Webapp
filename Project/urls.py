
from django.urls import path, include
from . import views
from django.conf.urls import url
from fund import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', views.index, name='index'),
        path('home', views.home),
        path('addproject', views.addproject, name='addproject'),
        path('addproject/pic', views.django_image_and_file_upload_ajax),
        path('<int:prj_id>/details/', views.project),
        path('<int:prj_id>/addcomment/', views.addcomment),
        path('<int:prj_id>/like/', views.addlike),
        path('<int:prj_id>/dislike/', views.adddislike),
        path('<int:prj_id>/deletecomment/', views.deletecomment),
        path('<int:prj_id>/donate/', views.donate),
        path('<int:prj_id>/report/', views.addreport),
        path('<int:prj_id>/deleteproject/', views.deleteproject),
        path('<int:cat_id>/catProjects/', views.lisCategoryProjects),
        path('search/', views.django_search_ajax),
        path('logout/', views.logout),






        
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
