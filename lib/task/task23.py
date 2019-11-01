from lib.task.base import Task, MultipleChoiceTask
from typing import Dict


class Task23(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_23

        self.inverse_task: bool = 'утверждений являются ошибочными' in self.text.lower()
        self.lines = self.get_numbered_lines(blacklist=[
            'утверждений являются верными',
            'утверждений являются ошибочными',
            'Прочитайте текст',
        ])
        self.lines[-1] = self.split_lines(self.lines[-1])[0]
