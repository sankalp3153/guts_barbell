from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.WorkoutProgramListView.as_view(), name='program_list'),
    path('programs/<slug:slug>/', views.WorkoutProgramDetailView.as_view(), name='program_detail'),
    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('exercises/<slug:slug>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),
]
