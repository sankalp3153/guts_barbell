"""
Strength & hypertrophy analytics: 1RM estimation (Epley/Brzycki) and weekly
muscle-group set volume aggregation.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass(frozen=True)
class SetEntry:
    muscle_group: str
    weight_kg: float
    reps: int
    sets: int = 1


def estimate_one_rep_max(weight_kg: float, reps: int) -> float:
    if weight_kg <= 0 or reps <= 0:
        raise ValueError("weight_kg and reps must be positive")
    if reps == 1:
        return round(weight_kg, 2)
    # Epley formula for rep ranges 2-15
    return round(weight_kg * (1.0 + reps / 30.0), 2)


def calculate_session_tonnage(entries: Iterable[SetEntry]) -> float:
    total = 0.0
    for e in entries:
        total += e.weight_kg * e.reps * e.sets
    return round(total, 2)


def weekly_sets_by_muscle(entries: Iterable[SetEntry]) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for e in entries:
        counts[e.muscle_group] += e.sets
    return dict(counts)
