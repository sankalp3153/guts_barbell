from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Exercise, WorkoutProgram, WorkoutDay

class WorkoutProgramListView(ListView):
    """
    View for listing all workout programs.
    """
    model = WorkoutProgram
    template_name = 'workouts/program_list.html'
    context_object_name = 'programs'
    paginate_by = 9

    def get_queryset(self):
        queryset = WorkoutProgram.objects.filter(is_published=True).order_by('-created_at')
        query = self.request.GET.get('q')
        difficulty = self.request.GET.get('difficulty')
        duration = self.request.GET.get('duration')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        if duration:
            queryset = queryset.filter(duration_weeks=duration)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['difficulties'] = dict(WorkoutProgram.DIFFICULTY_CHOICES)
        context['durations'] = dict(WorkoutProgram.DURATION_CHOICES)
        return context

class WorkoutProgramDetailView(DetailView):
    """
    View for displaying a single workout program.
    """
    model = WorkoutProgram
    template_name = 'workouts/program_detail.html'
    context_object_name = 'program'

    def get_queryset(self):
        return WorkoutProgram.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout_days'] = self.object.workout_days.all().order_by('day_number')
        context['related_programs'] = WorkoutProgram.objects.filter(
            difficulty=self.object.difficulty,
            is_published=True
        ).exclude(id=self.object.id)[:3]
        return context

class ExerciseListView(ListView):
    """
    View for listing all exercises.
    """
    model = Exercise
    template_name = 'workouts/exercise_list.html'
    context_object_name = 'exercises'
    paginate_by = 12

    def get_queryset(self):
        queryset = Exercise.objects.all().order_by('name')
        query = self.request.GET.get('q')
        muscle_group = self.request.GET.get('muscle_group')
        difficulty = self.request.GET.get('difficulty')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(instructions__icontains=query)
            )

        if muscle_group:
            queryset = queryset.filter(muscle_group=muscle_group)

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['muscle_groups'] = dict(Exercise.MUSCLE_GROUP_CHOICES)
        context['difficulties'] = dict(Exercise.DIFFICULTY_CHOICES)
        return context

class ExerciseDetailView(DetailView):
    """
    View for displaying a single exercise.
    """
    model = Exercise
    template_name = 'workouts/exercise_detail.html'
    context_object_name = 'exercise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_exercises'] = Exercise.objects.filter(
            muscle_group=self.object.muscle_group
        ).exclude(id=self.object.id)[:4]
        return context
