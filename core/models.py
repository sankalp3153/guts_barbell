from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    """
    Site-wide settings for the Blood and Guts fitness website.
    """
    site_name = models.CharField(_('Site Name'), max_length=100, default='Blood and Guts')
    site_description = models.TextField(_('Site Description'), blank=True)
    site_logo = models.ImageField(_('Site Logo'), upload_to='site_images/', blank=True, null=True)
    favicon = models.ImageField(_('Favicon'), upload_to='site_images/', blank=True, null=True)
    footer_text = models.TextField(_('Footer Text'), blank=True)
    facebook_url = models.URLField(_('Facebook URL'), blank=True, null=True)
    twitter_url = models.URLField(_('Twitter URL'), blank=True, null=True)
    instagram_url = models.URLField(_('Instagram URL'), blank=True, null=True)
    youtube_url = models.URLField(_('YouTube URL'), blank=True, null=True)

    class Meta:
        verbose_name = _('site settings')
        verbose_name_plural = _('site settings')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            return SiteSettings.objects.first()
        return super().save(*args, **kwargs)
