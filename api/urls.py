from api.views import BasketAPIViews
from django.urls import path


urlpatterns = [
    path('basket/', BasketAPIViews.as_view()),
]
