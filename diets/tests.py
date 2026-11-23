from django.test import SimpleTestCase

from diets.nutrition import calculate_macros, summarize_meals


class NutritionCalculatorTests(SimpleTestCase):
    def test_macro_plan_muscle_gain_and_cut(self):
        bulk = calculate_macros(weight_kg=75, height_cm=178, age=24, sex="male", activity="moderate", goal="muscle_gain")
        cut = calculate_macros(weight_kg=75, height_cm=178, age=24, sex="male", activity="moderate", goal="weight_loss")
        self.assertGreater(bulk.target_calories, cut.target_calories)
        self.assertEqual(bulk.protein_grams, 150)
        self.assertEqual(cut.protein_grams, 165)

    def test_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            calculate_macros(weight_kg=-5, height_cm=170, age=25)

    def test_meal_summary(self):
        totals = summarize_meals([
            {"calories": 600, "protein_grams": 45, "carbs_grams": 65, "fat_grams": 15},
            {"calories": 750, "protein_grams": 55, "carbs_grams": 80, "fat_grams": 20},
        ])
        self.assertEqual(totals["calories"], 1350)
        self.assertEqual(totals["protein_grams"], 100)
