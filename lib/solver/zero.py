from lib.task import Task
from lib.solver.base import BaseSolver
from lib.solver.sberbank import SberbankSolver
from typing import List, Dict, Any


class ZeroSolver(BaseSolver):
    def get_task_type(self) -> str:
        return Task.TYPE_UNKNOWN

    def solve(self, task: Task) -> Any:
        question = task.data['question']

        if question['type'] == 'choice':
            answer = 'UNK'

        elif question['type'] == 'multiple_choice':
            answer = ['UNK']

        elif question['type'] == 'matching':
            answer = {left['id']: 'UNK' for left in question['left']}

        elif question['type'] == 'text':
            answer = 'UNK'

        else:
            raise RuntimeError('Unknown question type: {}'.format(question['type']))

        return answer


class ZeroSberbankSolver(BaseSolver):
    def __init__(self, task_types: List[type]):
        self.task_types: List[type] = task_types
        self.zero: ZeroSolver = ZeroSolver()
        self.sberbank: SberbankSolver = SberbankSolver()

    def get_task_type(self) -> str:
        return Task.TYPE_UNKNOWN

    def solve(self, task: Task) -> Any:
        for task_type in self.task_types:
            if isinstance(task, task_type):
                return self.sberbank.solve(task)

        return self.zero.solve(task)
