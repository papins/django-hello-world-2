def settings(request):
    """
    Adds project settings to the context.

    """
    from django.conf import settings

    context_extras = {}
    context_extras['SETTINGS'] = settings

    return context_extras
