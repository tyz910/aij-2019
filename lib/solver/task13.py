import numpy as np
from lib.task import Task, Task13
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.speller import Speller

from typing import Any, Optional


class Task13Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None, speller: Optional[Speller] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

    def get_task_type(self) -> str:
        return Task.TYPE_13

    def solve(self, task: Task13) -> Any:
        lines = []
        line_words = []

        for line, words in zip(task.lines, task.words):
            is_known_spelled = self.speller.is_known(words[0])
            is_known_separated = self.speller.is_known(words[1].split(' ')[1])

            if is_known_spelled and not is_known_separated:
                return words[0]

            if is_known_separated and not is_known_spelled:
                continue

            lines.append(line)
            line_words.append(words)

        scores = []
        for line, words in zip(lines, line_words):
            scores.append(self.bert.get_replace_proba(line.replace('[MASK]', words[0]), words[0], words[1]))

        if scores:
            return line_words[int(np.argmin(scores))][0]
        else:
            return task.words[0][0]
