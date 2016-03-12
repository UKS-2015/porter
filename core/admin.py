from django.contrib import admin
from django.apps import apps

core_app = apps.get_app_config('core')

for model_name, model in core_app.models.items():
    admin.site.register(model)
