import numpy as np
from lib.task import Task, Task16
from lib.solver.base import BaseSolver
from lib.util.bert import Bert

from typing import List, Optional


class Task16Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

    def get_task_type(self) -> str:
        return Task.TYPE_16

    def solve(self, task: Task16) -> List[str]:
        scores = np.array([self.get_one_comma_score(line) for line in task.lines])
        return [str(i + 1) for i in np.argsort(-scores)[:task.num_choices]]

    def get_one_comma_score(self, text: str) -> float:
        words = text.split(' ')

        scores = []
        num_commas = 0
        for i in range(1, len(words)):
            candidate = ' '.join(words[:i]) + ' [MASK] ' + ' '.join(words[i:])
            score = self.bert.get_word_in_text_scores(candidate, ',')[0]
            if score > 0.95:
                num_commas += 1
            scores.append(score)

        max_score = max(scores)

        if num_commas == 0:
            return max_score
        elif num_commas == 1:
            return 1.0 + max_score
        else:
            return 0.0
