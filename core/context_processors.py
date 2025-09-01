from decouple import config


def global_context(request):
    thecnical = False
    if request.user.groups.filter(name__icontains='tecnico'):
        thecnical = True

    return {
        'enterprise_name': config('ENTERPRISE_NAME'),
        'url_logo': config('URL_LOGO'),
        'url_favicon': config('URL_FAVICON'),
        'thecnical': thecnical
    }
