from api.views import BasketAPIViews
from api.views import ClearSessionAPIViews
from django.urls import path


urlpatterns = [
    path('basket/', BasketAPIViews.as_view(), name='basket'),
    path('clear/', ClearSessionAPIViews.as_view())
]
