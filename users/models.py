from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom user model for Blood and Guts fitness website.
    Extends the built-in AbstractUser to add additional fields.
    """
    bio = models.TextField(_('Biography'), blank=True)
    profile_image = models.ImageField(_('Profile Image'), upload_to='profile_images/', blank=True, null=True)
    is_trainer = models.BooleanField(_('Trainer Status'), default=False, help_text=_('Designates whether this user can create workout programs and diets.'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username
