from django.test import TestCase
from .scoring import calculate_score
from datetime import date, timedelta

class ScoringTests(TestCase):
    def test_overdue_task_gets_high_urgency(self):
        task = {
            "title": "Old",
            "due_date": (date.today() - timedelta(days=2)).isoformat(),
            "estimated_hours": 3,
            "importance": 5,
            "dependencies": []
        }
        score = calculate_score(task, strategy="smart")
        self.assertTrue(score >= 100)  # overdue should add big urgency

    def test_quick_task_bonus(self):
        task = {
            "title": "Quick",
            "due_date": (date.today() + timedelta(days=10)).isoformat(),
            "estimated_hours": 1,
            "importance": 3,
            "dependencies": []
        }
        score = calculate_score(task, strategy="smart")
        # quick tasks should get the effort bonus relative to non-quick tasks
        self.assertTrue(score >= 10)

    def test_strategy_impact_vs_fast(self):
        task = {
            "title": "X",
            "due_date": (date.today() + timedelta(days=5)).isoformat(),
            "estimated_hours": 4,
            "importance": 9,
            "dependencies": []
        }
        impact_score = calculate_score(task, strategy="impact")
        fast_score = calculate_score(task, strategy="fast")
        self.assertTrue(impact_score > fast_score)
