"""
Nutrition & daily macro calculation utilities (Mifflin-St Jeor TDEE model).
"""

from dataclasses import dataclass
from typing import Dict, Iterable

ACTIVITY_MULTIPLIERS: Dict[str, float] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "athlete": 1.9,
}

GOAL_CALORIE_DELTA: Dict[str, int] = {
    "weight_loss": -450,
    "maintenance": 0,
    "muscle_gain": 300,
    "athletic": 200,
}


@dataclass(frozen=True)
class MacroPlan:
    bmr: int
    tdee: int
    target_calories: int
    protein_grams: int
    fat_grams: int
    carbs_grams: int

    def to_dict(self) -> Dict[str, int]:
        return {
            "bmr": self.bmr,
            "tdee": self.tdee,
            "target_calories": self.target_calories,
            "protein_grams": self.protein_grams,
            "fat_grams": self.fat_grams,
            "carbs_grams": self.carbs_grams,
        }


def calculate_macros(
    weight_kg: float,
    height_cm: float,
    age: int,
    sex: str = "male",
    activity: str = "moderate",
    goal: str = "muscle_gain",
) -> MacroPlan:
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        raise ValueError("weight_kg, height_cm, and age must be positive")
    if activity not in ACTIVITY_MULTIPLIERS:
        raise ValueError(f"Unsupported activity level: {activity}")
    if goal not in GOAL_CALORIE_DELTA:
        raise ValueError(f"Unsupported goal: {goal}")

    sex_offset = 5 if sex.lower() == "male" else -161
    bmr = round((10 * weight_kg) + (6.25 * height_cm) - (5 * age) + sex_offset)
    tdee = round(bmr * ACTIVITY_MULTIPLIERS[activity])
    target_calories = max(1200, tdee + GOAL_CALORIE_DELTA[goal])

    protein_g = round(weight_kg * (2.2 if goal == "weight_loss" else 2.0))
    fat_g = round((target_calories * 0.25) / 9)
    remaining_kcal = max(0, target_calories - (protein_g * 4) - (fat_g * 9))
    carbs_g = round(remaining_kcal / 4)

    return MacroPlan(
        bmr=bmr,
        tdee=tdee,
        target_calories=target_calories,
        protein_grams=protein_g,
        fat_grams=fat_g,
        carbs_grams=carbs_g,
    )


def summarize_meals(meals: Iterable[Dict[str, int]]) -> Dict[str, int]:
    totals = {"calories": 0, "protein_grams": 0, "carbs_grams": 0, "fat_grams": 0}
    for meal in meals:
        for key in totals:
            totals[key] += int(meal.get(key) or 0)
    return totals
