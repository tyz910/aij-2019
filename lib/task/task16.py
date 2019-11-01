import re
from lib.task.base import Task, MultipleChoiceTask
from typing import Dict, List


class Task16(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_16

        self.num_choices: int = 1
        if re.search(r'(номера\sпредложений|два\sпредложения)', self.text.lower()) is not None:
            self.num_choices = 2

        self.lines: List[str] = [c['text'] for c in self.choices]

    def get_score(self, answer: List[str]) -> float:
        a = set(self.answer)
        b = set(answer)

        u = len(a.union(b))
        i = len(a.intersection(b))

        if u > 0:
            return self.score * (i / u)
        else:
            return 0.0
