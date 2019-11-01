from lib.task.base import Task, MultipleChoiceTask
from typing import Dict, List, Optional


class Task22(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_22

        self.correct = True
        if 'противоречат содержанию текста' in self.text.lower():
            self.correct = False
        if 'не соответствуют содержанию текста' in self.text.lower():
            self.correct = False

        self.lines = self.get_numbered_lines(blacklist=[
            'содержанию текста',
        ])
        self.lines[-1] = self.split_lines(self.lines[-1])[0]
