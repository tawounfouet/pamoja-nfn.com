# analytics/admin.py

from django.contrib import admin
from .models import PageView

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'operating_system', 'browser', 'view_count', 'viewed_at', 'last_time_viewed', 'page_requested', 
                    'hostname', 'city', 'postal', 'region', 'country', 'loc', 'org', 'timezone_info',
                    
                    )
    list_filter = ('country', 'operating_system', 'browser', 'viewed_at', 'view_count')
    search_fields = ('ip_address', 'hostname', 'city', 'region', 'country', 'page_requested')
