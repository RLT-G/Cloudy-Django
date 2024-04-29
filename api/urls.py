from api.views import BasketAPIViews
from api.views import ClearSessionAPIViews
from api.views import CheckPromocodeAPIViews
from django.urls import path


urlpatterns = [
    path('basket/', BasketAPIViews.as_view(), name='basket'),
    path('clear/', ClearSessionAPIViews.as_view()),
    path('check_promocode/', CheckPromocodeAPIViews.as_view(), name='check_promo')
]
