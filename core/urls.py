from django.urls import path
from . import api, views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    # JSON API endpoints
    path('api/health/', api.health_check, name='api_health'),
    path('api/workouts/', api.list_workouts_api, name='api_workouts'),
    path('api/diets/', api.list_diets_api, name='api_diets'),
    path('api/macros/calculate/', api.calculate_macros_api, name='api_macros_calculate'),
]
