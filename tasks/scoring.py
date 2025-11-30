from datetime import date, datetime

# List of holidays (ISO format)
HOLIDAYS = {
    "2025-01-01",
    "2025-01-14",
    "2025-03-14",
    "2025-10-02",
}

def is_weekend(d: date) -> bool:
    return d.weekday() >= 5  # Saturday = 5, Sunday = 6

def is_holiday(d: date) -> bool:
    return d.isoformat() in HOLIDAYS

from datetime import datetime, date

def calculate_task_score(task):
    score = 0

    due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
    today = date.today()

    days_left = (due - today).days

    if days_left < 0:
        score += 70
    elif days_left <= 2:
        score += 40
    elif days_left <= 5:
        score += 20

    score += task.get("importance", 5) * 5

    hours = task.get("estimated_hours", 1)
    if hours <= 2:
        score += 10
    elif hours <= 4:
        score += 5

    deps = task.get("dependencies", [])
    if len(deps) > 0:
        score += len(deps) * 5

    return score

def calculate_score(task, strategy="smart"):
    """
    Main scoring logic with Date Intelligence.
    strategy = smart | deadline | impact | fast
    """

    today = date.today()
    due = date.fromisoformat(task["due_date"])
    days_left = (due - today).days

    # --------------------------
    # 1. URGENCY BASE SCORE
    # --------------------------
    urgency = 0

    if days_left < 0:
        urgency += 100
    elif days_left <= 2:
        urgency += 50
    elif days_left <= 5:
        urgency += 30
    else:
        urgency += 10

    # Weekend boost
    if is_weekend(due):
        urgency += 15

    # Holiday boost
    if is_holiday(due):
        urgency += 25

    # --------------------------
    # 2. IMPORTANCE WEIGHTING
    # --------------------------
    importance = task.get("importance", 5) * 5

    # --------------------------
    # 3. EFFORT BONUS
    # --------------------------
    hours = task.get("estimated_hours", 3)
    effort_bonus = 10 if hours <= 2 else 5 if hours <= 4 else 0

    # --------------------------
    # 4. STRATEGY HANDLING
    # --------------------------
    if strategy == "deadline":
        return urgency

    if strategy == "impact":
        return importance

    if strategy == "fast":
        return (20 - hours) + effort_bonus

    # --------------------------
    # 5. SMART BALANCED SCORE (DEFAULT)
    # --------------------------
    return urgency + importance + effort_bonus
