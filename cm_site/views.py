from django.shortcuts import render, redirect
# Для описания request в функциях
from django.core.handlers.wsgi import WSGIRequest
from . models import CustomUser, Tracks, Prices, Banners
from . forms import SearchForm

def index(request: WSGIRequest):
    data = {
        'user': request.user,
        'user_data': CustomUser.objects.all()
    }
    # return render(request, 'cm_site/index.html', data)
    return redirect('store')

def store(request: WSGIRequest):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text_field']
            if text is None or text == "":
                current_tracks = Tracks.objects.all()
            else:
                current_tracks = Tracks.objects.filter(track_name__icontains=text)
            data = {
                'user': request.user,
                'tracks': current_tracks,
                'prices': Prices.objects.all()[0],
                'search_form': form,
                'banners': Banners.objects.all()
            }
            return render(request, 'cm_site/store.html', data)
        else:
            text = None
    else:
        form = SearchForm()
    data = {
        'user': request.user,
        'tracks': Tracks.objects.all().order_by('-id'),
        'prices': Prices.objects.all()[0],
        'search_form': form,
        'banners': Banners.objects.all()
    }
    return render(request, 'cm_site/store.html', data)

def store_track(request: WSGIRequest, track_id: int, track_name: str):
    data = {
       'id': track_id,
       'name': track_name
    }
    return render(request, 'cm_site/track.html', data)

def not_developed(request: WSGIRequest):
    return render(request, 'cm_site/track.html')
    