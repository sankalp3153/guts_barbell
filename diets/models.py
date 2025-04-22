from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

class DietPlan(models.Model):
    """
    Diet plan model for complete nutrition plans.
    """
    GOAL_CHOICES = (
        ('weight_loss', _('Weight Loss')),
        ('muscle_gain', _('Muscle Gain')),
        ('maintenance', _('Maintenance')),
        ('performance', _('Performance')),
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
    goal = models.CharField(_('Goal'), max_length=20, choices=GOAL_CHOICES)
    duration_weeks = models.IntegerField(_('Duration (weeks)'), choices=DURATION_CHOICES, default=8)
    calories_per_day = models.PositiveIntegerField(_('Calories per day'), blank=True, null=True)
    protein_grams = models.PositiveIntegerField(_('Protein (g)'), blank=True, null=True)
    carbs_grams = models.PositiveIntegerField(_('Carbohydrates (g)'), blank=True, null=True)
    fat_grams = models.PositiveIntegerField(_('Fat (g)'), blank=True, null=True)
    featured_image = models.ImageField(_('Featured Image'), upload_to='diet_images/', blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    is_published = models.BooleanField(_('Published'), default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.CASCADE, related_name='diet_plans')

    class Meta:
        verbose_name = _('diet plan')
        verbose_name_plural = _('diet plans')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('diets:diet_detail', kwargs={'slug': self.slug})

class Meal(models.Model):
    """
    Meal model for individual meals within a diet plan.
    """
    MEAL_TYPE_CHOICES = (
        ('breakfast', _('Breakfast')),
        ('lunch', _('Lunch')),
        ('dinner', _('Dinner')),
        ('snack', _('Snack')),
        ('pre_workout', _('Pre-Workout')),
        ('post_workout', _('Post-Workout')),
    )

    diet_plan = models.ForeignKey(DietPlan, verbose_name=_('Diet Plan'), on_delete=models.CASCADE, related_name='meals')
    name = models.CharField(_('Name'), max_length=100)
    meal_type = models.CharField(_('Meal Type'), max_length=20, choices=MEAL_TYPE_CHOICES)
    description = models.TextField(_('Description'), blank=True)
    calories = models.PositiveIntegerField(_('Calories'), blank=True, null=True)
    protein_grams = models.PositiveIntegerField(_('Protein (g)'), blank=True, null=True)
    carbs_grams = models.PositiveIntegerField(_('Carbohydrates (g)'), blank=True, null=True)
    fat_grams = models.PositiveIntegerField(_('Fat (g)'), blank=True, null=True)
    image = models.ImageField(_('Image'), upload_to='meal_images/', blank=True, null=True)
    order = models.PositiveIntegerField(_('Order'))

    class Meta:
        verbose_name = _('meal')
        verbose_name_plural = _('meals')
        ordering = ['diet_plan', 'order']
        unique_together = ['diet_plan', 'order']

    def __str__(self):
        return f'{self.diet_plan.title} - {self.name}'

class Recipe(models.Model):
    """
    Recipe model for detailed meal recipes.
    """
    meal = models.ForeignKey(Meal, verbose_name=_('Meal'), on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(_('Title'), max_length=200)
    ingredients = models.TextField(_('Ingredients'))
    instructions = models.TextField(_('Instructions'))
    prep_time = models.PositiveIntegerField(_('Preparation Time (minutes)'), blank=True, null=True)
    cook_time = models.PositiveIntegerField(_('Cooking Time (minutes)'), blank=True, null=True)
    servings = models.PositiveIntegerField(_('Servings'), default=1)
    calories_per_serving = models.PositiveIntegerField(_('Calories per Serving'), blank=True, null=True)
    image = models.ImageField(_('Image'), upload_to='recipe_images/', blank=True, null=True)

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')
        ordering = ['meal', 'title']

    def __str__(self):
        return self.title
