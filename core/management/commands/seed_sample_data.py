from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from diets.models import DietPlan, Meal
from workouts.models import Exercise, WorkoutDay, WorkoutExercise, WorkoutProgram

User = get_user_model()


class Command(BaseCommand):
    help = "Seed sample trainer, barbell workout program, and diet plan for local development."

    def handle(self, *args, **options):
        trainer, created = User.objects.get_or_create(
            username="coach_sankalp",
            defaults={
                "email": "coach@gutsbarbell.local",
                "is_trainer": True,
                "is_staff": True,
                "bio": "Strength & hypertrophy programming specialist.",
            },
        )
        if created:
            trainer.set_password("ChangeMe!2026")
            trainer.save()

        bench, _ = Exercise.objects.get_or_create(
            slug="barbell-bench-press",
            defaults={
                "name": "Barbell Bench Press",
                "description": "Primary horizontal pressing compound movement.",
                "instructions": "Retract scapula, lower barbell to mid-chest, press explosively.",
                "difficulty": "intermediate",
                "muscle_group": "chest",
                "created_by": trainer,
            },
        )
        squat, _ = Exercise.objects.get_or_create(
            slug="back-squat",
            defaults={
                "name": "Barbell Back Squat",
                "description": "Foundational lower-body strength lift.",
                "instructions": "Brace core, break at hips and knees to parallel, drive through mid-foot.",
                "difficulty": "intermediate",
                "muscle_group": "legs",
                "created_by": trainer,
            },
        )

        program, _ = WorkoutProgram.objects.get_or_create(
            slug="guts-upper-lower-8-week",
            defaults={
                "title": "Guts 8-Week Upper / Lower Strength Split",
                "description": "Progressive overload barbell split targeting strength and hypertrophy.",
                "difficulty": "intermediate",
                "duration_weeks": 8,
                "is_published": True,
                "author": trainer,
            },
        )

        day1, _ = WorkoutDay.objects.get_or_create(
            program=program,
            day_number=1,
            defaults={"name": "Day 1: Upper Power", "description": "Heavy horizontal push/pull focus."},
        )
        WorkoutExercise.objects.get_or_create(
            workout_day=day1,
            order=1,
            defaults={"exercise": bench, "sets": 4, "reps": "5-6", "rest_time": "120-180s"},
        )

        day2, _ = WorkoutDay.objects.get_or_create(
            program=program,
            day_number=2,
            defaults={"name": "Day 2: Lower Power", "description": "Primary squat and posterior chain work."},
        )
        WorkoutExercise.objects.get_or_create(
            workout_day=day2,
            order=1,
            defaults={"exercise": squat, "sets": 4, "reps": "5", "rest_time": "180s"},
        )

        diet, _ = DietPlan.objects.get_or_create(
            slug="lean-hypertrophy-2800",
            defaults={
                "title": "Lean Hypertrophy 2800 kcal Plan",
                "description": "High-protein nutrition protocol for steady lean mass gain.",
                "goal": "muscle_gain",
                "duration_weeks": 8,
                "calories_per_day": 2800,
                "protein_grams": 180,
                "carbs_grams": 330,
                "fat_grams": 80,
                "is_published": True,
                "author": trainer,
            },
        )
        Meal.objects.get_or_create(
            diet_plan=diet,
            order=1,
            defaults={
                "name": "Oats, Whey & Almond Butter Bowl",
                "meal_type": "breakfast",
                "calories": 680,
                "protein_grams": 46,
                "carbs_grams": 78,
                "fat_grams": 19,
            },
        )
        self.stdout.write(self.style.SUCCESS("Seeded Guts Barbell demo data."))
