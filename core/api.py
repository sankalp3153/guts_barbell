import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from diets.models import DietPlan
from diets.nutrition import calculate_macros
from workouts.models import WorkoutProgram


@require_GET
def health_check(_request):
    return JsonResponse({"status": "ok", "service": "guts-barbell"})


@require_GET
def list_workouts_api(request):
    qs = WorkoutProgram.objects.filter(is_published=True).select_related("author")
    difficulty = request.GET.get("difficulty")
    if difficulty:
        qs = qs.filter(difficulty=difficulty)

    items = [
        {
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "difficulty": p.difficulty,
            "duration_weeks": p.duration_weeks,
            "author": p.author.username,
        }
        for p in qs[:50]
    ]
    return JsonResponse({"count": len(items), "results": items})


@require_GET
def list_diets_api(request):
    qs = DietPlan.objects.filter(is_published=True).select_related("author")
    goal = request.GET.get("goal")
    if goal:
        qs = qs.filter(goal=goal)

    items = [
        {
            "id": d.id,
            "title": d.title,
            "slug": d.slug,
            "goal": d.goal,
            "calories_per_day": d.calories_per_day,
            "protein_grams": d.protein_grams,
            "carbs_grams": d.carbs_grams,
            "fat_grams": d.fat_grams,
            "author": d.author.username,
        }
        for d in qs[:50]
    ]
    return JsonResponse({"count": len(items), "results": items})


@csrf_exempt
@require_POST
def calculate_macros_api(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
        plan = calculate_macros(
            weight_kg=float(body["weight_kg"]),
            height_cm=float(body["height_cm"]),
            age=int(body["age"]),
            sex=str(body.get("sex", "male")),
            activity=str(body.get("activity", "moderate")),
            goal=str(body.get("goal", "muscle_gain")),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse(plan.to_dict(), status=200)
