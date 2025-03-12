from django import forms
from django.contrib import admin
from taggit.admin import TagAdmin

from import_export import fields, widgets
from django.utils.text import slugify


from .models import (
    Category, SubCategory, CustomTag, TaggedListing, 
    Listing, ContactInformation, SocialMediaLinks, BusinessHours,
    Review, Media, Analytics
)
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Define resources for each model
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

# class SubCategoryResource(resources.ModelResource):
#     class Meta:
#         model = SubCategory
#         fields = ('id', 'name', 'category', 'description')

class SubCategoryResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=widgets.ForeignKeyWidget(Category, 'name')
    )
    
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category', 'description')
        export_order = ('id', 'name', 'category', 'description')
    
    def before_import_row(self, row, **kwargs):
        """
        Try to get or create the category based on name
        """
        category_name = row.get('category')
        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                row['category'] = category.id
            except Category.DoesNotExist:
                # Optionally create a new category
                category = Category.objects.create(
                    name=category_name, 
                    slug=slugify(category_name)
                )
                row['category'] = category.id


class CustomTagResource(resources.ModelResource):
    class Meta:
        model = CustomTag
        fields = ('id', 'name', 'slug')

# class ListingResource(resources.ModelResource):
#     class Meta:
#         model = Listing
#         fields = ('id', 'title', 'category', 'subcategory', 'description', 'type', 'status', 'created_at')

# class ListingResource(resources.ModelResource):
#     category = fields.Field(
#         column_name='category',
#         attribute='category',
#         widget=widgets.ForeignKeyWidget(Category, 'name')
#     )
    
#     subcategory = fields.Field(
#         column_name='subcategory',
#         attribute='subcategory',
#         widget=widgets.ForeignKeyWidget(SubCategory, 'name')
#     )
    
#     class Meta:
#         model = Listing
#         fields = ('id', 'title', 'category', 'subcategory', 'description', 'type', 'status', 'created_at')
#         export_order = ('id', 'title', 'category', 'subcategory', 'description', 'type', 'status', 'created_at')
    
#     def before_import_row(self, row, **kwargs):
#         """
#         Try to get or create the category and subcategory based on names
#         """
#         # Handle category name to ID conversion
#         category_name = row.get('category')
#         if category_name:
#             try:
#                 category = Category.objects.get(name=category_name)
#                 row['category'] = category.id
#             except Category.DoesNotExist:
#                 # Optionally create a new category
#                 category = Category.objects.create(name=category_name, slug=slugify(category_name))
#                 row['category'] = category.id
        
#         # Handle subcategory name to ID conversion
#         subcategory_name = row.get('subcategory')
#         if subcategory_name and row.get('category'):
#             try:
#                 subcategory = SubCategory.objects.get(
#                     name=subcategory_name, 
#                     category_id=row['category']
#                 )
#                 row['subcategory'] = subcategory.id
#             except SubCategory.DoesNotExist:
#                 # Optionally create a new subcategory if category exists
#                 try:
#                     category = Category.objects.get(id=row['category'])
#                     subcategory = SubCategory.objects.create(
#                         name=subcategory_name,
#                         slug=slugify(subcategory_name),
#                         category=category
#                     )
#                     row['subcategory'] = subcategory.id
#                 except Category.DoesNotExist:
#                     pass

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
    
    class Meta:
        model = Listing
        fields = ('title', 'category', 'subcategory', 'description', 'type', 'status', 'created_at')  # ID removed
        export_order = ('title', 'category', 'subcategory', 'description', 'type', 'status', 'created_at')  # ID removed
        #import_id_fields = ('title',)  # Use title as identifier
        skip_unchanged = True
        report_skipped = False
    
    def before_import_row(self, row, **kwargs):
        """
        Try to get or create the category and subcategory based on names
        """
        # Handle category name to ID conversion
        category_name = row.get('category')
        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                row['category'] = category.id
            except Category.DoesNotExist:
                category = Category.objects.create(name=category_name, slug=slugify(category_name))
                row['category'] = category.id
        
        # Handle subcategory name to ID conversion
        subcategory_name = row.get('subcategory')
        if subcategory_name and row.get('category'):
            try:
                subcategory = SubCategory.objects.get(
                    name=subcategory_name, 
                    category_id=row['category']
                )
                row['subcategory'] = subcategory.id
            except SubCategory.DoesNotExist:
                try:
                    category = Category.objects.get(id=row['category'])
                    subcategory = SubCategory.objects.create(
                        name=subcategory_name,
                        slug=slugify(subcategory_name),
                        category=category
                    )
                    row['subcategory'] = subcategory.id
                except Category.DoesNotExist:
                    pass

class ContactInformationResource(resources.ModelResource):
    class Meta:
        model = ContactInformation
        fields = ('id', 'listing', 'contact_email', 'mobile_phone', 'preferred_contact')

class SocialMediaLinksResource(resources.ModelResource):
    class Meta:
        model = SocialMediaLinks
        fields = ('id', 'listing', 'facebook', 'instagram', 'twitter', 'linkedin')

class BusinessHoursResource(resources.ModelResource):
    class Meta:
        model = BusinessHours
        fields = ('id', 'listing', 'monday_open', 'monday_close', 'monday_closed',
                  'tuesday_open', 'tuesday_close', 'tuesday_closed',
                  'wednesday_open', 'wednesday_close', 'wednesday_closed',
                  'thursday_open', 'thursday_close', 'thursday_closed',
                  'friday_open', 'friday_close', 'friday_closed',
                  'saturday_open', 'saturday_close', 'saturday_closed',
                  'sunday_open', 'sunday_close', 'sunday_closed')

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
class ListingAdmin(ImportExportModelAdmin):
    resource_class = ListingResource
    list_display = ('title', 'category', 'type', 'status', 'get_contact_email',
        'get_phone', 'average_rating', 'get_tags', 'created_at')
    list_filter = ('status', 'type', 'category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'average_rating')
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
class SubCategoryAdmin(ImportExportModelAdmin):
    resource_class = SubCategoryResource
    list_display = ('id' , 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('category', 'name')


class SubCategoryResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=widgets.ForeignKeyWidget(Category, 'name')
    )
    
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category', 'description')
        export_order = ('id', 'name', 'category', 'description')
    
    def before_import_row(self, row, **kwargs):
        """
        Try to get or create the category based on name
        """
        category_name = row.get('category')
        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                row['category'] = category.id
            except Category.DoesNotExist:
                # Optionally create a new category
                category = Category.objects.create(
                    name=category_name, 
                    slug=slugify(category_name)
                )
                row['category'] = category.id


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

@admin.register(BusinessHours)
class BusinessHoursAdmin(ImportExportModelAdmin):
    resource_class = BusinessHoursResource
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