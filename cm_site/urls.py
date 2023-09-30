from django.urls import path, include
from allauth.account.views import ConfirmEmailView
from . import views

urlpatterns = [
    path('', view=views.index, name='home'),
    path('index/', view=views.index, name='index'),
    path('store/', view=views.store, name='store'),
    path('accounts/', include('allauth.urls')),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email')
]
