from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name',  'phone', 'address', 'country', 'bio']
    list_filter = [ 'country']
    search_fields = ['user__username', 'full_name', 'phone', 'address', 'country']
    #readonly_fields = ['verified']

    def has_add_permission(self, request):
        # Prevent direct addition of Profiles through the admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Optional: Allow or prevent deletion of Profile objects through the admin
        return True

    def get_readonly_fields(self, request, obj=None):
        # Make fields readonly based on conditions or admin settings
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # When editing an existing object
            return readonly_fields + ('user', 'verified')
        return readonly_fields

admin.site.register(Profile, ProfileAdmin)