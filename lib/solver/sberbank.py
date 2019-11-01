from lib.task import Task
from lib.solver.base import BaseSolver
from lib.sberbank.solution import CuttingEdgeStrongGeneralAI
from typing import Any, Optional, List


class SberbankSolver(BaseSolver):
    def __init__(self, solver_ids: Optional[List[int]] = None):
        self.ai = CuttingEdgeStrongGeneralAI(solver_ids)

    def get_task_type(self) -> str:
        return Task.TYPE_UNKNOWN

    def solve(self, task: Task) -> Any:
        answers = self.ai.take_exam({
            'tasks': [
                task.data
            ]
        })

        return answers[task.id]
