from datetime import date, datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .scoring import calculate_task_score, calculate_score

@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Expecting: { "tasks": [...], "strategy": "deadline" }
    tasks = data.get("tasks", [])
    strategy = data.get("strategy", "smart")

    results = []

    for task in tasks:
        # call correct scoring logic
        score = calculate_score(task, strategy)
        task["score"] = score
        results.append(task)

    # sort results
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return JsonResponse(results, safe=False)


@csrf_exempt
def suggest_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    try:
        body = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    tasks = body.get("tasks", [])
    strategy = body.get("strategy", "smart")

    if not tasks:
        return JsonResponse({"error": "No tasks provided"}, status=400)

    results = []

    for task in tasks:
        score = calculate_score(task, strategy)

        # Build explanation
        explanation = ""
        if task["importance"] >= 8:
            explanation += "High importance. "
        if (date.fromisoformat(task["due_date"]) - date.today()).days <= 2:
            explanation += "Near deadline. "
        if task["estimated_hours"] <= 2:
            explanation += "Quick task. "

        results.append({
            "title": task["title"],
            "score": score,
            "explanation": explanation.strip(),
            "due_date": task["due_date"],
            "importance": task["importance"],
            "estimated_hours": task["estimated_hours"]
        })

    # sort top 3
    results.sort(key=lambda x: x["score"], reverse=True)
    return JsonResponse(results[:3], safe=False)
