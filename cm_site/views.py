from django.shortcuts import render, redirect, get_object_or_404
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
                current_tracks = Tracks.objects.all().order_by('-priority')
            else:
                current_tracks = Tracks.objects.filter(track_name__icontains=text).order_by('-priority')
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
        'tracks': Tracks.objects.all().order_by('-priority'),
        'prices': Prices.objects.all()[0],
        'search_form': form,
        'banners': Banners.objects.all()
    }
    return render(request, 'cm_site/store.html', data)


def store_track(request: WSGIRequest, track_id: int):
    track = get_object_or_404(Tracks, id=track_id)
    data = {
        'user': request.user,
        'id': track_id,
        'track': track
    }
    return render(request, 'cm_site/track.html', data)


def not_developed(request: WSGIRequest):
    request.session.flush()
    return render(request, 'cm_site/comingsoon.html')
    

def basket(request: WSGIRequest):
    basket = request.session.get('basket', None)

    track_names = [item['track_name'] for item in basket]

    tracks_in_basket = Tracks.objects.filter(track_name__in=track_names)
    data = {
        'tracks': tracks_in_basket,
        'basket': basket
    }
    return render(request, 'cm_site/basket.html', data)