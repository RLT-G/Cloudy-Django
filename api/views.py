# Rest framework
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.forms import model_to_dict
from django.core.handlers.wsgi import WSGIRequest

from api.utils import has_duplicate_dicts

from rest_framework.permissions import AllowAny
# Models
# from api1.models import PhraseModel

# Serializers
# from api1.serializers import FirstSerializer
# from api1.serializers import SecondSerializers
# from api1.serializers import ThirdSerializers


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
                basket.append({'track_name': track_name, 'license': license})
                if has_duplicate_dicts(basket):
                    answer = {
                        'status': 'Error',
                        'data': 'Already in cart'
                    }
                    return Response(answer)
                requests.session['basket'] = basket
            else:
                requests.session['basket'] = [{'track_name': track_name, 'license': license}]
            answer = {
                'status': 'OK',
                'data': f'add {track_name} to basket'
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



