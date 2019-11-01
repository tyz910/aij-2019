from lib.task import Task, Task23
from lib.solver.base import BaseSolver
from typing import List, Dict, Any


class Task23Solver(BaseSolver):
    def __init__(self):
        pass

    def get_task_type(self) -> str:
        return Task.TYPE_23

    def solve(self, task: Task23) -> Any:
        return None
