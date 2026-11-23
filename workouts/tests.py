from django.contrib.auth import get_user_model
from django.test import TestCase

from workouts.analytics import SetEntry, calculate_session_tonnage, estimate_one_rep_max, weekly_sets_by_muscle
from workouts.models import Exercise, WorkoutProgram

User = get_user_model()


class WorkoutAnalyticsTests(TestCase):
    def test_epley_one_rep_max(self):
        self.assertEqual(estimate_one_rep_max(100.0, 1), 100.0)
        self.assertEqual(estimate_one_rep_max(100.0, 6), 120.0)
        with self.assertRaises(ValueError):
            estimate_one_rep_max(0, 5)

    def test_tonnage_and_weekly_sets(self):
        entries = [
            SetEntry("chest", 100.0, 5, sets=4),
            SetEntry("chest", 30.0, 10, sets=3),
            SetEntry("legs", 140.0, 5, sets=4),
        ]
        self.assertEqual(calculate_session_tonnage(entries), 5700.0)
        self.assertEqual(weekly_sets_by_muscle(entries), {"chest": 7, "legs": 4})

    def test_program_slug_auto_generation(self):
        user = User.objects.create_user(username="trainer1", password="Password!123", is_trainer=True)
        program = WorkoutProgram.objects.create(
            title="Powerbuilding Block A",
            description="Compound lifts + accessories",
            author=user,
            is_published=True,
        )
        self.assertEqual(program.slug, "powerbuilding-block-a")
        ex = Exercise.objects.create(
            name="Romanian Deadlift",
            description="Posterior chain hinge",
            instructions="Hinge hips back with soft knees",
            muscle_group="legs",
            created_by=user,
        )
        self.assertEqual(ex.slug, "romanian-deadlift")
