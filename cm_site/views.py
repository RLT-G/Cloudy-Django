from django.shortcuts import render

# Create your views here.

def index(request):
    data = {
        'user': request.user
    }
    return render(request, 'cm_site/index.html', data)

def store(request):
    data = {
        'user': request.user
    }
    return render(request, 'cm_site/store.html', data)