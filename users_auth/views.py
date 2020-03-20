from django.shortcuts import render


# Create your views here.
def index(request):
    
    return render(request, 'users_auth/index.html')

def categories(request):
    
    return render(request, 'users_auth/categories.html')
