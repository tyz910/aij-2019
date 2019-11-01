from lib.solver.base import BaseSolver
from lib.task import Task, Task04
from lib.util.stress import Stress

from typing import Optional, List, Tuple


class Task04Solver(BaseSolver):
    def __init__(self, stress: Optional[Stress] = None):
        if stress is None:
            stress = Stress()
        self.stress: Stress = stress

    def get_task_type(self) -> str:
        return Task.TYPE_04

    def solve(self, task: Task04) -> str:
        unknown: List[Tuple[str, int]] = []
        for word, stress in task.words:
            stresses = self.stress.from_vocab(word)
            if stresses is not None:
                if len(stresses) > 1:
                    unknown.append((word, stress))

                if stress not in stresses:
                    return word

        for word, stress in unknown:
            stresses = self.stress.from_model(word)
            if stress not in stresses:
                return word

        if len(unknown) > 0:
            return unknown[0][0]
        else:
            return task.words[0][0]
