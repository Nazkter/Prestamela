from django.contrib import admin
from prestapi.models import *
from django.apps import apps
# Register your models here.
for model in apps.get_app_config('prestapi').models.values():
    admin.site.register(model)
