import numpy as np
from lib.task import Task, Task03
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.sentence_encoder import SentenceEncoder

from typing import Optional, Any


class Task03Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None, sentence_encoder: Optional[SentenceEncoder] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if sentence_encoder is None:
            sentence_encoder = SentenceEncoder()
        self.sentence_encoder: SentenceEncoder = sentence_encoder

    def get_task_type(self) -> str:
        return Task.TYPE_03

    def solve(self, task: Task03) -> Any:
        text = task.lines[task.line_num]

        sims = []
        for i, choice in enumerate(task.choices):
            sim = self.sentence_encoder.get_similarity(choice['text'], text)[0]
            sims.append(sim)

        max_idx = int(np.argmax(sims))
        return [str(max_idx + 1)]
