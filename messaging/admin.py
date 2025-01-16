from django.contrib import admin
from .models import Conversation, Message, MessageAttachment

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at', 'read_at')
    fields = ('sender', 'content', 'status', 'created_at', 'read_at')

class AttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 0
    fields = ('file', 'file_name', 'file_type', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

#@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('participants__email',)
    inlines = [MessageInline]
    filter_horizontal = ('participants',)

#@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'content', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('content', 'sender__email')
    readonly_fields = ('created_at', 'read_at')
    inlines = [AttachmentInline]
    actions = ['mark_as_read', 'mark_as_delivered']

    def mark_as_read(self, request, queryset):
        for message in queryset:
            message.mark_as_read()
    mark_as_read.short_description = "Marquer comme lu"

    def mark_as_delivered(self, request, queryset):
        for message in queryset:
            message.mark_as_delivered()
    mark_as_delivered.short_description = "Marquer comme délivré"

#@admin.register(MessageAttachment)
class MessageAttachmentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'message', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('file_name',)
    readonly_fields = ('uploaded_at',)