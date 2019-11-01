from lib.task import Task, Task24
from lib.solver.base import BaseSolver
from typing import List, Dict, Any


class Task24Solver(BaseSolver):
    def __init__(self):
        pass

    def get_task_type(self) -> str:
        return Task.TYPE_24

    def solve(self, task: Task24) -> Any:
        return None
