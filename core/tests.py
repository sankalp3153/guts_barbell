import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from workouts.models import WorkoutProgram

User = get_user_model()


class CoreApiTests(TestCase):
    def test_health_endpoint(self):
        resp = self.client.get("/api/health/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ok")

    def test_workouts_api_returns_only_published(self):
        u = User.objects.create_user(username="coach", password="Password!123", is_trainer=True)
        WorkoutProgram.objects.create(title="Live Split", description="x", author=u, is_published=True)
        WorkoutProgram.objects.create(title="Draft Split", description="y", author=u, is_published=False)

        resp = self.client.get("/api/workouts/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["title"], "Live Split")

    def test_macro_calculator_api(self):
        resp = self.client.post(
            "/api/macros/calculate/",
            data=json.dumps({"weight_kg": 78, "height_cm": 180, "age": 23, "goal": "muscle_gain"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("target_calories", body)
        self.assertGreater(body["target_calories"], 2000)

        bad = self.client.post("/api/macros/calculate/", data="{}", content_type="application/json")
        self.assertEqual(bad.status_code, 400)
