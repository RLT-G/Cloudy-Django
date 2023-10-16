from django.shortcuts import render
# Для описания request в функциях
from django.core.handlers.wsgi import WSGIRequest
from . models import CustomUser


# Create your views here.
def index(request: WSGIRequest):
    data = {
        'user': request.user,
        'user_data': CustomUser.objects.all()
    }
    # if request.method == 'GET':
    #     print('GETGETGET')
    return render(request, 'cm_site/index.html', data)

def store(request: WSGIRequest):
    data = {
        'user': request.user
    }
    return render(request, 'cm_site/store.html', data)