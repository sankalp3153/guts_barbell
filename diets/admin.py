from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import DietPlan, Meal, Recipe

class RecipeInline(admin.TabularInline):
    model = Recipe
    extra = 1

class MealInline(admin.TabularInline):
    model = Meal
    extra = 1
    show_change_link = True

@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal', 'duration_weeks', 'author', 'is_published', 'created_at')
    list_filter = ('goal', 'duration_weeks', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [MealInline]
    actions = ['publish_plans', 'unpublish_plans']

    def publish_plans(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, _(f'{queryset.count()} diet plans were successfully published.'))
    publish_plans.short_description = _('Publish selected diet plans')

    def unpublish_plans(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, _(f'{queryset.count()} diet plans were successfully unpublished.'))
    unpublish_plans.short_description = _('Unpublish selected diet plans')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'diet_plan', 'meal_type', 'calories', 'order')
    list_filter = ('diet_plan', 'meal_type')
    search_fields = ('name', 'description', 'diet_plan__title')
    inlines = [RecipeInline]

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'meal', 'prep_time', 'cook_time', 'servings', 'calories_per_serving')
    list_filter = ('meal__diet_plan', 'meal')
    search_fields = ('title', 'ingredients', 'instructions', 'meal__name')
