# Rest framework
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.forms import model_to_dict
from django.core.handlers.wsgi import WSGIRequest


# Models
# from api1.models import PhraseModel

# Serializers
# from api1.serializers import FirstSerializer
# from api1.serializers import SecondSerializers
# from api1.serializers import ThirdSerializers


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


class BasketAPIViews(APIView):
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
        if track_name is None:
            answer = {
                'status': 'Error',
                'data': 'No name entered'
            }
        else:
            if 'basket' in requests.session:
                basket = requests.session.get('basket')
                basket.append(track_name);
                requests.session['basket'] = basket
            else:
                requests.session['basket'] = [track_name]
            answer = {
                'status': 'OK',
                'data': f'add {track_name} to basket'
            }
        return Response(answer)

