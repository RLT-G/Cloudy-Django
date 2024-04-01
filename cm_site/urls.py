from django.urls import path, include
from allauth.account.views import ConfirmEmailView
from . import views

urlpatterns = [
    path('', view=views.index, name='home'),
    path('index/', view=views.index, name='index'),
    path('store/', view=views.store, name='store'),
    path('store/<int:track_id>/', view=views.store_track, name='store_track'),
    path('cart/', view=views.basket, name='cart'),
    path('accounts/', include('allauth.urls')),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('notdeveloped/', view=views.not_developed, name='not_developed')
]
