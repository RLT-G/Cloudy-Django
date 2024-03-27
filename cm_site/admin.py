from django.contrib import admin
from . models import *
# Register your models here.
cm_site_models = [CustomUser, Prices, Moods, Tracks, Banners, Tags]
for model in cm_site_models:
    admin.site.register(model)