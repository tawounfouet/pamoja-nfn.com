from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Location

@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ('city', 'region', 'country', 'address')
    list_filter = ('country', 'region')
    search_fields = ('city', 'address', 'country')
    
    fieldsets = (
        ('Location Details', {
            'fields': ('city', 'region', 'country', 'address')
        }),
        ('Coordinates', {
            'fields': ('coordinates',),
            'classes': ('collapse',),
            'description': 'Location coordinates in {lat: float, lng: float} format'
        }),
    )
    
    readonly_fields = ('get_coordinates_display',)
    
    def get_coordinates_display(self, obj):
        if obj.coordinates:
            return f"Latitude: {obj.coordinates.get('lat')}, Longitude: {obj.coordinates.get('lng')}"
        return "No coordinates set"
    get_coordinates_display.short_description = 'Coordinates Display'