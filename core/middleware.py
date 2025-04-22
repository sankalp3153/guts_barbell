from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class TrainerRequiredMiddleware:
    """
    Middleware to check if a user has trainer permissions for certain views.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check if the view requires trainer permissions
        if hasattr(view_func, 'trainer_required') and view_func.trainer_required:
            if not request.user.is_authenticated:
                messages.error(request, "You need to be logged in to access this page.")
                return redirect(reverse('users:login'))
            
            if not request.user.is_trainer and not request.user.is_staff:
                messages.error(request, "You need trainer permissions to access this page.")
                return redirect(reverse('core:home'))
        
        return None

def trainer_required(view_func):
    """
    Decorator to mark views that require trainer permissions.
    """
    view_func.trainer_required = True
    return view_func
