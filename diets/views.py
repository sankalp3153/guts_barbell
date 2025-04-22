from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import DietPlan, Meal, Recipe

class DietPlanListView(ListView):
    """
    View for listing all diet plans.
    """
    model = DietPlan
    template_name = 'diets/diet_list.html'
    context_object_name = 'diets'
    paginate_by = 9

    def get_queryset(self):
        queryset = DietPlan.objects.filter(is_published=True).order_by('-created_at')
        query = self.request.GET.get('q')
        goal = self.request.GET.get('goal')
        duration = self.request.GET.get('duration')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        if goal:
            queryset = queryset.filter(goal=goal)

        if duration:
            queryset = queryset.filter(duration_weeks=duration)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goals'] = dict(DietPlan.GOAL_CHOICES)
        context['durations'] = dict(DietPlan.DURATION_CHOICES)
        return context

class DietPlanDetailView(DetailView):
    """
    View for displaying a single diet plan.
    """
    model = DietPlan
    template_name = 'diets/diet_detail.html'
    context_object_name = 'diet'

    def get_queryset(self):
        return DietPlan.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = self.object.meals.all().order_by('order')
        context['related_diets'] = DietPlan.objects.filter(
            goal=self.object.goal,
            is_published=True
        ).exclude(id=self.object.id)[:3]
        return context
