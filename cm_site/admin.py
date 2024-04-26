from django.contrib import admin
from . models import *
# Register your models here.
cm_site_models = [
    CustomUser, 
    Tracks, 
    PurchasedTrack,
    Prices,
    Moods, 
    Banners, 
    Tags, 
    ErrorReport,
    SignContracts,
    NoSignContracts,
    Promocode
]
for model in cm_site_models:
    admin.site.register(model)
    