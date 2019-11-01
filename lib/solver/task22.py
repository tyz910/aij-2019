from lib.task import Task, Task22
from lib.solver.base import BaseSolver
from typing import List, Dict, Any


class Task22Solver(BaseSolver):
    def __init__(self):
        pass

    def get_task_type(self) -> str:
        return Task.TYPE_22

    def solve(self, task: Task22) -> Any:
        return None
