from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Exercise, WorkoutProgram, WorkoutDay, WorkoutExercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group', 'difficulty', 'created_by', 'created_at')
    list_filter = ('muscle_group', 'difficulty', 'created_at')
    search_fields = ('name', 'description', 'instructions')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1
    autocomplete_fields = ['exercise']

class WorkoutDayInline(admin.TabularInline):
    model = WorkoutDay
    extra = 1
    show_change_link = True

@admin.register(WorkoutProgram)
class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration_weeks', 'author', 'is_published', 'created_at')
    list_filter = ('difficulty', 'duration_weeks', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [WorkoutDayInline]
    actions = ['publish_programs', 'unpublish_programs']

    def publish_programs(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, _(f'{queryset.count()} programs were successfully published.'))
    publish_programs.short_description = _('Publish selected programs')

    def unpublish_programs(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, _(f'{queryset.count()} programs were successfully unpublished.'))
    unpublish_programs.short_description = _('Unpublish selected programs')

@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'day_number')
    list_filter = ('program',)
    search_fields = ('name', 'description', 'program__title')
    inlines = [WorkoutExerciseInline]

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'workout_day', 'sets', 'reps', 'order')
    list_filter = ('workout_day__program', 'workout_day')
    search_fields = ('exercise__name', 'notes', 'workout_day__name')
    autocomplete_fields = ['exercise', 'workout_day']
