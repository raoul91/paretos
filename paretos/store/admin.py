from django.contrib import admin
from .models import ParetosUser


@admin.register(ParetosUser)
class ParetosUserAdmin(admin.ModelAdmin):
    pass
