from .models import SiteSettings

def site_settings(request):
    """
    Context processor to make site settings available in all templates.
    """
    try:
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings.objects.create(site_name="Blood and Guts")
    except:
        settings = None
    
    return {'site_settings': settings}
