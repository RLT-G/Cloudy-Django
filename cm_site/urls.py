from django.urls import path, include
from allauth.account.views import ConfirmEmailView
from . import views

urlpatterns = [
    # Лендос
    path('', view=views.index, name='home'),
    path('index/', view=views.index, name='index'),

    # Магаз
    path('store/', view=views.store, name='store'),
    path('store/<int:track_id>/', view=views.store_track, name='store_track'),

    # Корзина и оплата
    path('cart/', view=views.basket, name='cart'),
    path('checkout/', view=views.checkout, name='checkout'),
    path('success/', view=views.success, name='success'),
    path('cancel/', view=views.cancel, name='cancel'),

    # Аккаунты
    path('accounts/', include('allauth.urls')),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),

    # Дополнительные
    path('notdeveloped/', view=views.not_developed, name='not_developed')
]
