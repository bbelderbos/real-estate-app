from django.contrib import admin
from .models import PropertyForRent


@admin.register(PropertyForRent)
class PropertyForRentAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'source_site']
