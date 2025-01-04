from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Language, SocialMediaPlatform, Notification

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'verified', 'date_registered', 'reputation_score', 'last_active')
    list_filter = ('verified', 'date_registered', 'is_public')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'bio')
    readonly_fields = ('date_registered', 'verification_date', 'last_active')
    filter_horizontal = ('languages', 'social_media_platforms')

    def user_info(self, obj):
        return format_html(
            '<div><strong>{}</strong><br>{}</div>',
            obj.user.get_full_name(),
            obj.user.email
        )
    user_info.short_description = 'Utilisateur'

    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user', 'bio', 'profile_image', 'is_public')
        }),
        ('Vérification', {
            'fields': ('verified', 'verification_date', 'verified_by')
        }),
        ('Détails', {
            'fields': ('contact_info', 'social_media_links', 'location')
        }),
        ('Compétences et réseaux', {
            'fields': ('languages', 'social_media_platforms')
        }),
        ('Statistiques', {
            'fields': ('reputation_score', 'date_registered', 'last_active')
        }),
    )

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(SocialMediaPlatform)
class SocialMediaPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url', 'icon')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'read', 'created_at', 'priority')
    list_filter = ('notification_type', 'read', 'created_at', 'priority')
    search_fields = ('user__email', 'title', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Informations de base', {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('État', {
            'fields': ('read', 'is_email_sent', 'priority')
        }),
        ('Relations', {
            'fields': ('related_object_type', 'related_object_id')
        }),
        ('Horodatage', {
            'fields': ('created_at',)
        }),
    )