from core.models import PorterUser
from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

core_app = apps.get_app_config('core')

for model_name, model in core_app.models.items():
    admin.site.register(model)
