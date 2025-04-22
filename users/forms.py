from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information.
    """
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_image']
