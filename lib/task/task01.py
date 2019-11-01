from lib.task.base import Task, MultipleChoiceTask
from typing import Dict, List


class Task01(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_01

        self.lines: List[str] = self.get_numbered_lines(blacklist=[
            'Запишите номера этих предложений',
            'Укажите два предложения',
            'Укажите варианты ответов',
        ])
