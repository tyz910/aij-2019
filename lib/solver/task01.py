import numpy as np
from lib.task import Task, Task01
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.sentence_encoder import SentenceEncoder
from typing import List, Optional


class Task01Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None, sentence_encoder: Optional[SentenceEncoder] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if sentence_encoder is None:
            sentence_encoder = SentenceEncoder()
        self.sentence_encoder: SentenceEncoder = sentence_encoder

    def get_task_type(self) -> str:
        return Task.TYPE_01

    def solve(self, task: Task01) -> List[str]:
        text = ' '.join(task.lines)
        text_emb = self.bert.eval(text)

        sims = []
        for i, choice in enumerate(task.choices):
            choice_emb = self.bert.eval(choice['text'])
            sim1 = text_emb.get_similarity(choice_emb)
            sim2 = self.sentence_encoder.get_similarity(choice['text'], text)[0]
            sims.append(0.8 * np.mean(sim1[-5:-2]) + 0.2 * sim2)

        return list(sorted([str(task.choices[i]['id']) for i in np.argsort(-np.array(sims))[:2]]))
