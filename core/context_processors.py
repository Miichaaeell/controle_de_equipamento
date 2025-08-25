from decouple import config


def global_context(request):
    return {
        'enterprise_name': config('ENTERPRISE_NAME'),
        'url_logo': config('URL_LOGO'),
    }
