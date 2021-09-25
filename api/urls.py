from django.urls import re_path
from api.views import get_user_by_session

urlpatterns = [
    re_path(r'^get-user-by-session/?$', get_user_by_session, name = 'get-user-by-session')
]