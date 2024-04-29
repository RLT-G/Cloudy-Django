# Rest framework
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.forms import model_to_dict
from django.core.handlers.wsgi import WSGIRequest

# Utils
from api.utils import has_duplicate_dicts

# Permissions
from rest_framework.permissions import AllowAny

# Models
from cm_site.models import Prices, Promocode, AppliedPromocodes


class CheckPromocodeAPIViews(APIView):
    @staticmethod
    def post(request):
        if 'promocode' in request.data:
            if Promocode.objects.filter(promo_name=request.data.get('promocode')).exists() and \
                not AppliedPromocodes.objects.filter(user=request.user).filter(
                    promocode=Promocode.objects.get(promo_name=request.data.get('promocode'))
                ).exists():
                
                promocode_obj = Promocode.objects.get(promo_name=request.data.get('promocode'))

                answer = {
                    'status': 'OK',
                    'data': {
                        'data_create': promocode_obj.data_create,
                        'promo_discount': promocode_obj.promo_discount,
                        'promo_count': promocode_obj.promo_count
                    }
                }
            else:
                answer = {
                    'status': 'Error',
                    'data': 'Promocode doesnt exist'
                }
        else:
            answer = {
                'status': 'Error',
                'data': 'No promocode entered'
            }
        return Response(answer)
    

class BasketAPIViews(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(requests):
        if 'basket' in requests.session:
            answer = {
                'status': 'OK',
                'data': requests.session.get('basket')
            }
        else:
            answer = {
                'status': 'OK',
                'data': None
            }
        return Response(answer)
    
    @staticmethod
    def post(requests: WSGIRequest):
        prices = Prices.objects.all().first()
        prices = {
            'wav': prices.wav_license,
            'unlimited': prices.unlimited_license,
            'exclusive': prices.exclusive_license
        }
        track_name = requests.data.get('name', None)
        license = requests.data.get('license', None)
        if track_name is None or license is None:
            answer = {
                'status': 'Error',
                'data': 'No name or license entered'
            }
        elif not (license in ['wav', 'unlimited', 'exclusive']):
            answer = {
                'status': 'Error',
                'data': 'Invalid license'
            }
        else:
            if 'basket' in requests.session:
                basket = requests.session.get('basket')
                basket.append({'track_name': track_name, 'license': license, 'price': prices.get(license)})
                if has_duplicate_dicts(basket):
                    answer = {
                        'status': 'Error',
                        'data': 'Already in cart'
                    }
                    return Response(answer)
                requests.session['basket'] = basket
            else:
                requests.session['basket'] = [{'track_name': track_name, 'license': license, 'price': prices.get(license)}]
            answer = {
                'status': 'OK',
                'data': f'add {track_name} to basket'
            }
        return Response(answer)
    
    @staticmethod
    def delete(requests: WSGIRequest):
        track_name = requests.data.get('name', None)
        license = requests.data.get('license', None)
        if track_name is None or license is None:
            answer = {
                'status': 'Error',
                'data': 'No name or license entered'
            }
        elif not (license in ['wav', 'unlimited', 'exclusive']):
            answer = {
                'status': 'Error',
                'data': 'Invalid license'
            }
        else:
            if 'basket' in requests.session:
                basket = requests.session.get('basket')

                out_of_cart = True
                for track in basket:
                    if ('track_name', track_name) in track.items() and ('license', license) in track.items():
                        del basket[basket.index(track)]
                        out_of_cart = False
                requests.session['basket'] = basket
                if basket == []:
                    del requests.session['basket']

                if out_of_cart:
                    answer = {
                        'status': 'Error',
                        'data': 'Out of cart'
                    }                        
                else:
                    answer = {
                        'status': 'OK',
                        'data': f'Remove {track_name} from basket'
                    }     
            else:
                answer = {
                        'status': 'Error',
                        'data': 'Cart is empty'
                    }
        return Response(answer)
    

class ClearSessionAPIViews(APIView):
    @staticmethod
    def delete(requests):
        requests.session.flush()
        return Response({'answer': 'OK'})




# Накидал на рандомиче.
# class MainAPIViews(APIView):
    # @staticmethod
    # def get(requests):
        # data = PhraseModel.objects.all()
        # data_list = [
        #     {
        #         'number': str(el.number),
        #         'message': str(el.message),
        #         'data_created': str(el.data_created),
        #     }
        #     for el in data
        # ]
        # data = {
        #     'data': data_list
        # }
        # return Response({'answer': 'GET OK'})

    # @staticmethod
    # def post(requests: WSGIRequest):
        # try:
        # post_data = {
        #     "params": {
        #         'param1': requests.GET.get('param1', None)
        #     },
        #     "body": {
        #         'number': requests.data['number'],
        #         'message': requests.data['message']
        #     }
        # }
            #     # Установка значения в сессии
            # request.session['my_key'] = 'my_value'
            
            # # Получение значения из сессии
            # my_value = request.session.get('my_key', 'default_value')
            
            # # Удаление значения из сессии
            # if 'my_key' in request.session:
            #     del request.session['my_key']
        #     phrase = PhraseModel(number=post_data['number'], message=post_data['message'])
        #     answer = {
        #         'message': 'OK',
        #     }
        #     phrase.save()
        # except Exception as ex:
        #     answer = {
        #         'message': 'error'
        #     }
        #     print(ex)
        # return Response({'answer': {'status': 'POST OK', 'data': post_data}})



