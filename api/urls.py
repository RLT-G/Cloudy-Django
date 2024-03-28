from api.views import MainAPIViews
from django.urls import path


urlpatterns = [
    path('1/', MainAPIViews.as_view()),
]
