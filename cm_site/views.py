from django.shortcuts import render, redirect, get_object_or_404
# Для описания request в функциях
from django.core.handlers.wsgi import WSGIRequest
from . models import CustomUser, Tracks, Prices, Banners, PurchasedTrack
from . forms import SearchForm
from www import settings
from pprint import pprint
import stripe
from django.contrib.auth.decorators import login_required


def index(request: WSGIRequest):
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
    if basket is None:
        data = {

        }
        return render(request, 'cm_site/basket.html')
    else:

        track_names = [item['track_name'] for item in basket]

        tracks_in_basket = Tracks.objects.filter(track_name__in=track_names)
        data = {
            'tracks': tracks_in_basket,
            'basket': basket
        }
        return render(request, 'cm_site/basket.html', data)


@login_required
def checkout(request: WSGIRequest):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    basket = request.session.get('basket', None)
    if basket is None:
        return redirect('store')
    else:
        total_price = 0
        for track in basket:
            total_price += int(track['price'])
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Payment for CloudyMotion content',
                        },
                        'unit_amount': total_price * 100,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.CURRENT_DOMAIN + 'success/?session_id={CHECKOUT_SESSION_ID}',

            cancel_url=settings.CURRENT_DOMAIN + 'cancel/?session_id={CHECKOUT_SESSION_ID}',
        )

        return redirect(checkout_session.url, code=303)


def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session_id = request.GET.get('session_id')

    if not session_id:
        print('Нет сессии от stripe')
        return redirect('store')
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status != 'paid':
            print('Красавчик не оплатил')
            return redirect('store') 
        else:
            print('Красавчик оплатил')
            user = request.user
            basket = request.session.get('basket', None)
            if basket:
                for item in basket:
                    track = Tracks.objects.get(track_name=item['track_name'])
                    purchased_track = PurchasedTrack.objects.create(
                        user=user,
                        track=track
                    )
                    purchased_track.save()
                del request.session['basket']
            return redirect('store')  

    except Exception as e:
        print(str(e))   
        return redirect('store')


def cancel(request: WSGIRequest):
    print('cancel')
    return redirect('cart')
