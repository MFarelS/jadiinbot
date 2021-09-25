from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings

def url(request: WSGIRequest):
    return {
        'SERVER_URL': settings.SERVER_URL
    }