# Django
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.core.handlers.wsgi import WSGIRequest
from django.core.files.base import ContentFile
from django.urls import reverse

# Settings
from www import settings

# Models
from . models import (
    CustomUser, 
    Tracks,
    Prices,
    Banners,
    PurchasedTrack,
    NoSignContracts,
    Promocode,
    AppliedPromocodes
)

# Django Forms
from .forms import ErrorReportForm
from .forms import CustomUserForm
from . forms import SearchForm

# Utils
from api.utils import *
from io import BytesIO
import stripe
import math


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
                'banners': Banners.objects.all(),
                'basket': request.session.get('basket', None)
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
        'banners': Banners.objects.all(),
        'basket': request.session.get('basket', None)

    }
    return render(request, 'cm_site/store.html', data)

def store_track(request: WSGIRequest, track_id: int):
    track = get_object_or_404(Tracks, id=track_id)
    data = {
        'user': request.user,
        'id': track_id,
        'track': track,
        'prices': Prices.objects.all().first(),
        'basket': request.session.get('basket', None)
    }
    return render(request, 'cm_site/track.html', data)

def not_developed(request: WSGIRequest):
    return render(request, 'cm_site/comingsoon.html')

@login_required
def basket(request: WSGIRequest):
    basket = request.session.get('basket', None)
    if basket is None:
        data = {
            'user': request.user,
            'basket': None
        }
        return render(request, 'cm_site/basket.html')
    else:

        track_names = [item['track_name'] for item in basket]

        tracks_in_basket = Tracks.objects.filter(track_name__in=track_names)
        contracts = NoSignContracts.objects.all().first()
        data = {
            'user': request.user,
            'tracks': tracks_in_basket,
            'basket': basket,
            'wavcontarct': contracts.wav_license,
            'unlcontarct': contracts.unlimited_license,
            'exccontract': contracts.exclusive_license
        }
        return render(request, 'cm_site/basket.html', data)

@login_required
def checkout(request: WSGIRequest):
    if hasattr(request.user, 'artist_name') and not request.user.artist_name:
        request.user.artist_name = request.user.username
        request.user.save()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    basket = request.session.get('basket', None)
    promocode = request.GET.get('promocode', None)

    if basket is None:
        return redirect('store')
    else:
        total_price = 0
        for track in basket:
            total_price += int(track['price']) * 100
        if promocode is None:
            total_price +=  math.ceil(total_price * 0.029 + 30)
        else:
            if request.session.get('promo', None) is not None:
                del request.session['promo']

            if Promocode.objects.filter(promo_name=promocode).exists():
                promocode_obj = Promocode.objects.get(promo_name=promocode)
                if not AppliedPromocodes.objects.filter(user=request.user).filter(promocode=promocode_obj).exists():
                    if promocode_obj.promo_count > 0:
                        total_price = total_price - math.floor(total_price * (promocode_obj.promo_discount / 100))
                        total_price +=  math.ceil(total_price * 0.029 + 30)
                        request.session['promo'] = promocode_obj.promo_name

            else:
                total_price +=  math.ceil(total_price * 0.029 + 30)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Payment for CloudyMotion content',
                        },
                        'unit_amount': total_price,
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
            if request.session.get('promo', None) is not None:
                promo_obj = Promocode.objects.get(promo_name=request.session.get('promo'))
                AppliedPromocodes.objects.create(user=user, promocode=promo_obj).save()
                promo_obj.promo_count -= 1
                promo_obj.save()

            

            basket = request.session.get('basket', None)
            if basket:
                for item in basket:
                    track = Tracks.objects.get(track_name=item['track_name'])
                    output = createContract(request, track, item.get('license'))
                    with open(output, 'rb') as f:
                        contract_file = ContentFile(f.read())

                        purchased_track = PurchasedTrack.objects.create(
                            user=user,
                            track=track,
                            track_license=item.get('license')
                        )

                        purchased_track.contract.save(f'contract_{generate_unique_sequence()}.docx', contract_file)

                        purchased_track.save()
                        
                del request.session['basket']
            return redirect('store')  

    except Exception as e:
        print(str(e))   
        return redirect('store')

def cancel(request: WSGIRequest):
    print('cancel')
    return redirect('cart')


@login_required
@ratelimit(key='ip', rate='5/m', block=True)
def account(request: WSGIRequest):
    user_pt = PurchasedTrack.objects.filter(user=request.user)
    if request.method == 'GET':
        data = {
            'user_form': CustomUserForm(instance=request.user),
            'error_form': ErrorReportForm(),
            'redirect_on': 'default',
            'user_pt': user_pt,
            'basket': request.session.get('basket', None)
        }
        return render(request, 'cm_site/lk.html', data)
    elif request.method == 'POST':

        if 'form1-submit' in request.POST:
            user_form = CustomUserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                data = {
                    'user_form': CustomUserForm(instance=request.user),
                    'error_form': ErrorReportForm(),
                    'redirect_on': 'info',
                    'user_pt': user_pt,
                    'basket': request.session.get('basket', None)
                }
            else:
                data = {
                    'user_form': user_form,
                    'error_form': ErrorReportForm(),
                    'redirect_on': 'info',
                    'user_pt': user_pt,
                    'basket': request.session.get('basket', None)
                }
            return render(request, 'cm_site/lk.html', data)
            
        elif 'form2-submit' in request.POST:
            error_form = ErrorReportForm(request.POST, request.FILES)
            if error_form.is_valid():
                error_form.save()
                data = {
                    'user_form': CustomUserForm(instance=request.user),
                    'error_form': ErrorReportForm(),
                    'redirect_on': 'support',
                    'user_pt': user_pt,
                    'basket': request.session.get('basket', None)
                }
            else:
                data = {
                    'user_form': CustomUserForm(instance=request.user),
                    'error_form': error_form,
                    'redirect_on': 'support',
                    'user_pt': user_pt,
                    'basket': request.session.get('basket', None)
                }
            return render(request, 'cm_site/lk.html', data)
