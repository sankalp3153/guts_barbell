from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

class Exercise(models.Model):
    """
    Exercise model for individual exercises.
    """
    DIFFICULTY_CHOICES = (
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
    )

    MUSCLE_GROUP_CHOICES = (
        ('chest', _('Chest')),
        ('back', _('Back')),
        ('shoulders', _('Shoulders')),
        ('arms', _('Arms')),
        ('legs', _('Legs')),
        ('core', _('Core')),
        ('full_body', _('Full Body')),
    )

    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True, max_length=100)
    description = models.TextField(_('Description'))
    instructions = models.TextField(_('Instructions'))
    difficulty = models.CharField(_('Difficulty'), max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    muscle_group = models.CharField(_('Muscle Group'), max_length=20, choices=MUSCLE_GROUP_CHOICES)
    image = models.ImageField(_('Image'), upload_to='exercise_images/', blank=True, null=True)
    video_url = models.URLField(_('Video URL'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Created by'), on_delete=models.CASCADE, related_name='exercises')

    class Meta:
        verbose_name = _('exercise')
        verbose_name_plural = _('exercises')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('workouts:exercise_detail', kwargs={'slug': self.slug})

class WorkoutProgram(models.Model):
    """
    Workout program model for complete workout routines.
    """
    DIFFICULTY_CHOICES = (
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
    )

    DURATION_CHOICES = (
        (4, _('4 Weeks')),
        (8, _('8 Weeks')),
        (12, _('12 Weeks')),
        (16, _('16 Weeks')),
    )

    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True, max_length=200)
    description = models.TextField(_('Description'))
    difficulty = models.CharField(_('Difficulty'), max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    duration_weeks = models.IntegerField(_('Duration (weeks)'), choices=DURATION_CHOICES, default=8)
    featured_image = models.ImageField(_('Featured Image'), upload_to='program_images/', blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    is_published = models.BooleanField(_('Published'), default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.CASCADE, related_name='workout_programs')

    class Meta:
        verbose_name = _('workout program')
        verbose_name_plural = _('workout programs')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('workouts:program_detail', kwargs={'slug': self.slug})

class WorkoutDay(models.Model):
    """
    Workout day model for organizing exercises into days within a program.
    """
    program = models.ForeignKey(WorkoutProgram, verbose_name=_('Program'), on_delete=models.CASCADE, related_name='workout_days')
    name = models.CharField(_('Name'), max_length=100, help_text=_('e.g., Day 1: Chest and Triceps'))
    day_number = models.PositiveIntegerField(_('Day Number'))
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('workout day')
        verbose_name_plural = _('workout days')
        ordering = ['program', 'day_number']
        unique_together = ['program', 'day_number']

    def __str__(self):
        return f'{self.program.title} - {self.name}'

class WorkoutExercise(models.Model):
    """
    Junction model to connect exercises to workout days with specific sets, reps, etc.
    """
    workout_day = models.ForeignKey(WorkoutDay, verbose_name=_('Workout Day'), on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, verbose_name=_('Exercise'), on_delete=models.CASCADE, related_name='workout_exercises')
    sets = models.PositiveIntegerField(_('Sets'))
    reps = models.CharField(_('Reps'), max_length=50, help_text=_('e.g., 8-12 or 5,5,5'))
    rest_time = models.CharField(_('Rest Time'), max_length=50, help_text=_('e.g., 60-90 seconds'), blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    order = models.PositiveIntegerField(_('Order'))

    class Meta:
        verbose_name = _('workout exercise')
        verbose_name_plural = _('workout exercises')
        ordering = ['workout_day', 'order']
        unique_together = ['workout_day', 'order']

    def __str__(self):
        return f'{self.workout_day.name} - {self.exercise.name}'
