import numpy as np
from lib.task import Task, Task17
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.classifier import LgbClassifier, CtbClassifier
from typing import List, Set, Tuple, Optional


class Task17Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None):
        if bert is not None:
            self.bert = bert
        else:
            self.bert = Bert()

        self.model = LgbClassifier('task17')
        # self.model = CtbClassifier('task17')

    def get_task_type(self) -> str:
        return Task.TYPE_17

    def solve(self, task: Task17) -> List[str]:
        X, _ = self.get_Xy([task])
        preds = self.model.predict(X)[:, 1]

        return [str(i + 1) for i, score in enumerate(preds) if preds[i] > 0.5]

    def train(self, tasks: List[Task17], save: bool = True):
        X, y = self.get_Xy(tasks)
        self.model.train(X, y)

        if save:
            self.model.save()

    def get_Xy(self, tasks: List[Task17]) -> Tuple[np.array, Optional[np.array]]:
        X = []
        y = []

        for task in tasks:
            emb = self.bert.eval(task.sentence)
            token_positions = self.__get_token_positions(emb.token_ids, task.mask)
            token_embeddings = emb.get_token_embeddings(token_positions)
            # scores = self.get_comma_scores(task)

            for i, token_embedding in enumerate(token_embeddings):
                X.append(np.concatenate((
                    token_embedding,
                    # np.array(scores[i]),
                )))
                if y is not None and task.labels is not None:
                    y.append(task.labels[i])
                else:
                    y = None

        if y is not None:
            y = np.array(y)

        return np.array(X), y

    def __get_token_positions(self, token_ids: np.array, mask: List[bool]) -> List[int]:
        mask_num = 0
        token_positions = []

        for i, token_id in enumerate(token_ids):
            if token_id == 128:
                if mask[mask_num]:
                    token_positions.append(i)
                mask_num += 1
                if len(mask) < mask_num:
                    break

        return token_positions

    def nth_repl(self, s, sub, repl, nth):
        find = s.find(sub)
        # if find is not p1 we have found at least one match for the substring
        i = find != -1
        # loop util we find the nth or we find no match
        while find != -1 and i != nth:
            # find + 1 means we start at the last match start index + 1
            find = s.find(sub, find + 1)
            i += 1
        # if i  is equal to nth we found nth matches so replace
        if i == nth:
            return s[:find] + repl + s[find + len(sub):]
        return s

    def get_comma_scores(self, task):
        n = 0
        scores = []

        for mask in task.mask:
            n += 1
            if not mask:
                continue

            text = self.nth_repl(task.sentence, ',', ' [MASK] ', n)
            score = self.bert.get_word_in_text_scores(text, ',')
            scores.append(score)

        return scores
