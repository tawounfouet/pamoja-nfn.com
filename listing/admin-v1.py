from django import forms
from django.contrib import admin
from taggit.admin import TagAdmin

#from .models import Category, SubCategory, Tag, Listing, ContactInformation, SocialMediaLinks, Review, Media, Analytics

from .models import (
    Category, SubCategory, CustomTag, TaggedListing, 
    Listing, ContactInformation, SocialMediaLinks, BusinessHours,
    Review, Media, Analytics
)

class ListingAdminForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        widgets = {
            'tags': admin.widgets.FilteredSelectMultiple(
                verbose_name='Tags',
                is_stacked=False,
                attrs={'style': 'width: 90%; min-height: 250px;'}
            ),
        }



class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_active_listings_count')
    search_fields = ('name', 'description')
    inlines = [SubCategoryInline]

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'slug')
#     list_filter = ('category',)
#     search_fields = ('name', 'slug')
#     prepopulated_fields = {'slug': ('name',)}


class TaggedListingInline(admin.TabularInline):
    model = TaggedListing
    extra = 1

# Register the custom tag admin
@admin.register(CustomTag)
class CustomTagAdmin(TagAdmin):
    list_display = ('name',  'slug')
    #list_filter = ('category',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TaggedListingInline]


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at', 'updated_at')

class MediaInline(admin.TabularInline):
    model = Media
    extra = 0
    readonly_fields = ('uploaded_at',)

class AnalyticsInline(admin.TabularInline):
    model = Analytics
    readonly_fields = ('views', 'engagement_metrics', 'last_updated')
    can_delete = False
    max_num = 0


class ContactInformationInline(admin.StackedInline):
    model = ContactInformation
    can_delete = False
    verbose_name = "Informations de contact"
    verbose_name_plural = "Informations de contact"

class SocialMediaLinksInline(admin.StackedInline):
    model = SocialMediaLinks
    can_delete = False
    verbose_name = "Réseaux sociaux"
    verbose_name_plural = "Réseaux sociaux"


class BusinessHoursInline(admin.StackedInline):
    model = BusinessHours
    can_delete = False
    fieldsets = (
        ('Lundi', {
            'fields': (
                ('monday_open', 'monday_close'),
                'monday_closed',
            )
        }),
        ('Mardi', {
            'fields': (
                ('tuesday_open', 'tuesday_close'),
                'tuesday_closed',
            )
        }),
        ('Mercredi', {
            'fields': (
                ('wednesday_open', 'wednesday_close'),
                'wednesday_closed',
            )
        }),
        ('Jeudi', {
            'fields': (
                ('thursday_open', 'thursday_close'),
                'thursday_closed',
            )
        }),
        ('Vendredi', {
            'fields': (
                ('friday_open', 'friday_close'),
                'friday_closed',
            )
        }),
        ('Samedi', {
            'fields': (
                ('saturday_open', 'saturday_close'),
                'saturday_closed',
            )
        }),
        ('Dimanche', {
            'fields': (
                ('sunday_open', 'sunday_close'),
                'sunday_closed',
            )
        }),
    )

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    #form = ListingAdminForm
    list_display = ('title', 'category', 'type', 'status',  'get_contact_email',
        'get_phone', 'average_rating', 'get_tags', 'created_at')
    list_filter = ('status', 'type', 'category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'average_rating')
    # filter_horizontal = ('tags',)
    inlines = [ContactInformationInline, SocialMediaLinksInline, MediaInline, ReviewInline, AnalyticsInline, BusinessHoursInline]
    actions = ['activate_listings', 'deactivate_listings']

    def get_contact_email(self, obj):
        if hasattr(obj, 'contact_details'):
            return obj.contact_details.contact_email
        return "-" 
    get_contact_email.short_description = "Email"
    
    def get_phone(self, obj):
        if hasattr(obj, 'contact_details'):
            return obj.contact_details.mobile_phone
        return "-"
    get_phone.short_description = "Téléphone"

    
    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    get_tags.short_description = "Tags"

    

    def activate_listings(self, request, queryset):
        queryset.update(status=Listing.Status.ACTIVE)
    activate_listings.short_description = "Activer les annonces sélectionnées"

    def deactivate_listings(self, request, queryset):
        queryset.update(status=Listing.Status.INACTIVE)
    deactivate_listings.short_description = "Désactiver les annonces sélectionnées"



@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('category', 'name')

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('listing', 'contact_email', 'mobile_phone', 'preferred_contact')
    list_filter = ('preferred_contact',)
    search_fields = ('contact_email', 'mobile_phone')

@admin.register(SocialMediaLinks)
class SocialMediaLinksAdmin(admin.ModelAdmin):
    list_display = ('listing', 'facebook', 'instagram', 'twitter', 'linkedin')
    search_fields = ('listing__listing_title', 'listing__company_name')


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('listing', 'get_opening_status')
    search_fields = ('listing__title',)
    
    def get_opening_status(self, obj):
        from datetime import datetime
        now = datetime.now()
        day = now.strftime("%A").lower()
        if getattr(obj, f'{day}_closed'):
            return 'Fermé'
        return f'Ouvert de {getattr(obj, f"{day}_open")} à {getattr(obj, f"{day}_close")}'
    get_opening_status.short_description = "Statut d'ouverture"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'rating', 'moderation_status', 'is_visible')
    list_filter = ('moderation_status', 'is_visible', 'rating')
    search_fields = ('user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        for review in queryset:
            review.approve()
    approve_reviews.short_description = "Approuver les avis sélectionnés"

    def reject_reviews(self, request, queryset):
        queryset.update(moderation_status=Review.ModerationStatus.REJECTED)
    reject_reviews.short_description = "Rejeter les avis sélectionnés"

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'listing', 'type', 'is_primary')
    list_filter = ('type', 'is_primary')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at',)

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'views', 'last_updated')
    readonly_fields = ('views', 'engagement_metrics', 'last_updated')
    search_fields = ('listing__company_name',)