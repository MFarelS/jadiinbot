from django.urls import path
from main.views import IndexView, DashboardView, RegisterView

urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
    path('register/', RegisterView.as_view(), name = 'register'),
]