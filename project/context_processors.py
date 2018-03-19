from django.conf import settings


def google_analytics_code(request):
    return {
        'google_analytics_code': settings.GOOGLE_ANALYTICS_CODE
    }
