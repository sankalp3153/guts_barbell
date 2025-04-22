from django.urls import path
from . import views

app_name = 'diets'

urlpatterns = [
    path('', views.DietPlanListView.as_view(), name='diet_list'),
    path('<slug:slug>/', views.DietPlanDetailView.as_view(), name='diet_detail'),
]
