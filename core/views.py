from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from blogs.models import BlogPost
from workouts.models import WorkoutProgram
from diets.models import DietPlan

class HomeView(TemplateView):
    """
    Home page view for the Blood and Guts fitness website.
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_blogs'] = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
        context['featured_workouts'] = WorkoutProgram.objects.filter(is_published=True).order_by('-created_at')[:3]
        context['featured_diets'] = DietPlan.objects.filter(is_published=True).order_by('-created_at')[:3]
        return context

class AboutView(TemplateView):
    """
    About page view.
    """
    template_name = 'core/about.html'

class ContactView(TemplateView):
    """
    Contact page view.
    """
    template_name = 'core/contact.html'
