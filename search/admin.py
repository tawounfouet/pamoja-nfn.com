from django.contrib import admin
from .models import SearchDocument, SearchHistory

#@admin.register(SearchDocument)
class SearchDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'object_id', 'last_updated')
    list_filter = ('content_type', 'last_updated')
    search_fields = ('title', 'content')
    date_hierarchy = 'last_updated'

#@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'results_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'query')
    date_hierarchy = 'created_at'
