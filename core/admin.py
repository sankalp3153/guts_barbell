from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings

class BloodAndGutsAdminSite(admin.AdminSite):
    """
    Custom admin site with Berserk theme.
    """
    site_title = _('Blood and Guts Admin')
    site_header = _('Blood and Guts Administration')
    index_title = _('Site Management')

    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = 'css/admin.css'
        return context

admin_site = BloodAndGutsAdminSite(name='bloodandguts_admin')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General'), {
            'fields': ('site_name', 'site_description', 'site_logo', 'favicon', 'footer_text')
        }),
        (_('Social Media'), {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the site settings
        return False
