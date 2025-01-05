from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Profile, Language, Notification, ContactInfos, Socialinks
from authentication.models import User


class ProfileAdminForm(forms.ModelForm):
    user_first_name = forms.CharField(label="Prénom", max_length=150, required=False)
    user_last_name = forms.CharField(label="Nom", max_length=150, required=False)
    user_phone_number = forms.CharField(label="Numéro de téléphone", max_length=20, required=False)

    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['user_first_name'].initial = self.instance.user.first_name
            self.fields['user_last_name'].initial = self.instance.user.last_name
            self.fields['user_phone_number'].initial = self.instance.user.phone_number

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        if user:
            user.first_name = self.cleaned_data.get('user_first_name', user.first_name)
            user.last_name = self.cleaned_data.get('user_last_name', user.last_name)
            user.phone_number = self.cleaned_data.get('user_phone_number', user.phone_number)
            user.save()
        if commit:
            profile.save()
        return profile


class ContactInfosInline(admin.StackedInline):
    model = ContactInfos
    extra = 0
    verbose_name = "Informations de contact"
    verbose_name_plural = "Informations de contact"


class SocialinksInline(admin.StackedInline):
    model = Socialinks
    extra = 0
    verbose_name = "Réseaux sociaux"
    verbose_name_plural = "Réseaux sociaux"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ('user_info', 'verified', 'date_registered', 'reputation_score', 'last_active')
    list_filter = ('verified', 'date_registered', 'is_public')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'bio')
    readonly_fields = ('date_registered', 'verification_date', 'last_active')
    filter_horizontal = ('languages',)
    inlines = [ContactInfosInline, SocialinksInline]

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
        (_('Informations personnelles'), {
            'fields': ('user_first_name', 'user_last_name', 'user_phone_number'),
            'classes': ('collapse',)
        }),
        ('Contact et liens sociaux', {
            'fields': (),  # Ce champ sera géré par les inlines
        }),
        ('Vérification', {
            'fields': ('verified', 'verification_date', 'verified_by')
        }),
        ('Détails', {
            'fields': ('location',)
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


@admin.register(ContactInfos)
class ContactInfosAdmin(admin.ModelAdmin):
    list_display = ['profile', 'country', 'mobile_phone', 'whatsapp_number', 'contact_email', 'preferred_contact']
    search_fields = ['profile__user__username', 'contact_email']
    list_filter = ['country']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['mobile_phone'].help_text = "Format international requis (ex: +237612345678 pour le Cameroun)"
        form.base_fields['whatsapp_number'].help_text = "Format international requis (ex: +237612345678 pour le Cameroun)"
        return form
