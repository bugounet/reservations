from django.contrib import admin

# Register your models here.
from .models import UserPreference


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    search_fields = ['user__username']
