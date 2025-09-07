from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Difficulty = Literal["easy", "medium", "hard"]

@dataclass(frozen=True)
class Problem:
    id: int
    title: str
    tag: str
    difficulty: Difficulty
    box: int

def priority(box: int, difficulty: Difficulty) -> float:
    diff_penalty = {"easy": 0.0, "medium": -0.5, "hard": -1.0}[difficulty]
    return box + diff_penalty
