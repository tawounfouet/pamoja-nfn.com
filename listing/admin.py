from django import forms
from django.contrib import admin
from taggit.admin import TagAdmin
from django.utils.html import format_html


from import_export import fields, widgets

from .models import (
    Category, SubCategory, CustomTag, TaggedListing, 
    Listing, ContactInformation, SocialMediaLinks,
    Review, Media, Analytics, Location
)
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# register Location model


# Define resources for each model
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class SubCategoryResource(resources.ModelResource):

    category = fields.Field(
        column_name='category', 
        attribute='category',
        widget=widgets.ForeignKeyWidget(Category, 'name')
    )
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category', 'description')

class CustomTagResource(resources.ModelResource):
    class Meta:
        model = CustomTag
        fields = ('id', 'name', 'slug')



class ListingResource(resources.ModelResource):
    category = fields.Field(
        column_name='category', 
        attribute='category',
        widget=widgets.ForeignKeyWidget(Category, 'name')
    )
    
    subcategory = fields.Field(
        column_name='subcategory',
        attribute='subcategory', 
        widget=widgets.ForeignKeyWidget(SubCategory, 'name')
    )

    from datetime import datetime
    created_at = fields.Field(
        column_name='created_at',
        attribute='created_at',
        default=datetime.now
    )

    # mobile_phone = fields.Field(
    #     column_name='mobile_phone',
    #     attribute='contact_details__mobile_phone',
    # )

    class Meta:
        model = Listing
        fields = ('id', 'profile', 'title', 'category', 'subcategory',  'type', 'status',  'description', 'created_at')





class ContactInformationResource(resources.ModelResource):
    class Meta:
        model = ContactInformation
        fields = ('id', 'listing', 'contact_email', 'mobile_phone', 'preferred_contact')

class SocialMediaLinksResource(resources.ModelResource):
    class Meta:
        model = SocialMediaLinks
        fields = ('id', 'listing', 'facebook', 'instagram', 'twitter', 'linkedin')

# class BusinessHoursResource(resources.ModelResource):
#     class Meta:
#         model = BusinessHours
#         fields = ('id', 'listing', 'monday_open', 'monday_close', 'monday_closed',
#                   'tuesday_open', 'tuesday_close', 'tuesday_closed',
#                   'wednesday_open', 'wednesday_close', 'wednesday_closed',
#                   'thursday_open', 'thursday_close', 'thursday_closed',
#                   'friday_open', 'friday_close', 'friday_closed',
#                   'saturday_open', 'saturday_close', 'saturday_closed',
#                   'sunday_open', 'sunday_close', 'sunday_closed')

class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        fields = ('id', 'user', 'listing', 'rating', 'comment', 'moderation_status', 'is_visible', 'created_at')

class MediaResource(resources.ModelResource):
    class Meta:
        model = Media
        fields = ('id', 'listing', 'title', 'file', 'type', 'is_primary', 'uploaded_at')

class AnalyticsResource(resources.ModelResource):
    class Meta:
        model = Analytics
        fields = ('id', 'listing', 'views', 'engagement_metrics', 'last_updated')

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
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'get_active_listings_count')
    search_fields = ('name', 'description')
    inlines = [SubCategoryInline]

class TaggedListingInline(admin.TabularInline):
    model = TaggedListing
    extra = 1

@admin.register(CustomTag)
class CustomTagAdmin(TagAdmin, ImportExportModelAdmin):
    resource_class = CustomTagResource
    list_display = ('name', 'slug')
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

# class BusinessHoursInline(admin.StackedInline):
#     model = BusinessHours
#     can_delete = False
#     fieldsets = (
#         ('Lundi', {
#             'fields': (
#                 ('monday_open', 'monday_close'),
#                 'monday_closed',
#             )
#         }),
#         ('Mardi', {
#             'fields': (
#                 ('tuesday_open', 'tuesday_close'),
#                 'tuesday_closed',
#             )
#         }),
#         ('Mercredi', {
#             'fields': (
#                 ('wednesday_open', 'wednesday_close'),
#                 'wednesday_closed',
#             )
#         }),
#         ('Jeudi', {
#             'fields': (
#                 ('thursday_open', 'thursday_close'),
#                 'thursday_closed',
#             )
#         }),
#         ('Vendredi', {
#             'fields': (
#                 ('friday_open', 'friday_close'),
#                 'friday_closed',
#             )
#         }),
#         ('Samedi', {
#             'fields': (
#                 ('saturday_open', 'saturday_close'),
#                 'saturday_closed',
#             )
#         }),
#         ('Dimanche', {
#             'fields': (
#                 ('sunday_open', 'sunday_close'),
#                 'sunday_closed',
#             )
#         }),
#     )

@admin.register(Listing)
class ListingAdmin(ImportExportModelAdmin):
    resource_class = ListingResource
    list_display = ('title', 'image_thumbnail',  'category', 'subcategory', 
        'get_phone', 'updated_at', 'get_last_updated_by',  'created_at')
    list_filter = ('status', 'type', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'average_rating')
    inlines = [ContactInformationInline, SocialMediaLinksInline, MediaInline, ReviewInline, AnalyticsInline]
    actions = ['activate_listings', 'deactivate_listings']
    
    
    
    def get_last_updated_by(self, obj):
        if hasattr(obj, 'last_updated_by') and obj.last_updated_by:
            return obj.last_updated_by.username
        return '-'
    get_last_updated_by.short_description = 'Last Updated By'
    
    def save_model(self, request, obj, form, change):
        """
        Enregistre automatiquement l'utilisateur qui effectue la modification
        dans le champ last_updated_by
        """
        obj.last_updated_by = request.user
        super().save_model(request, obj, form, change)
    

    def image_thumbnail(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; " />', obj.logo.url)
        return format_html('<span>No Image</span>')
    image_thumbnail.short_description = 'Image'

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
class SubCategoryAdmin(ImportExportModelAdmin):
    resource_class = SubCategoryResource
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('category', 'name')

@admin.register(ContactInformation)
class ContactInformationAdmin(ImportExportModelAdmin):
    resource_class = ContactInformationResource
    list_display = ('listing', 'contact_email', 'mobile_phone', 'preferred_contact')
    list_filter = ('preferred_contact',)
    search_fields = ('contact_email', 'mobile_phone')

@admin.register(SocialMediaLinks)
class SocialMediaLinksAdmin(ImportExportModelAdmin):
    resource_class = SocialMediaLinksResource
    list_display = ('listing', 'facebook', 'instagram', 'twitter', 'linkedin')
    search_fields = ('listing__listing_title', 'listing__company_name')

# @admin.register(BusinessHours)
# class BusinessHoursAdmin(ImportExportModelAdmin):
#     resource_class = BusinessHoursResource
#     list_display = ('listing', 'get_opening_status')
#     search_fields = ('listing__title',)
    
#     def get_opening_status(self, obj):
#         from datetime import datetime
#         now = datetime.now()
#         day = now.strftime("%A").lower()
#         if getattr(obj, f'{day}_closed'):
#             return 'Fermé'
#         return f'Ouvert de {getattr(obj, f"{day}_open")} à {getattr(obj, f"{day}_close")}'
#     get_opening_status.short_description = "Statut d'ouverture"

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_class = ReviewResource
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
class MediaAdmin(ImportExportModelAdmin):
    resource_class = MediaResource
    list_display = ('title', 'listing', 'type', 'is_primary')
    list_filter = ('type', 'is_primary')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at',)

@admin.register(Analytics)
class AnalyticsAdmin(ImportExportModelAdmin):
    resource_class = AnalyticsResource
    list_display = ('listing', 'views', 'last_updated')
    readonly_fields = ('views', 'engagement_metrics', 'last_updated')
    search_fields = ('listing__company_name',)