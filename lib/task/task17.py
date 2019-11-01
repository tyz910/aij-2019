import re
from lib.task.base import Task, MultipleChoiceTask
from typing import Dict, List, Optional


class Task17(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_17

        self.sentence: str = self._to_line(self.text)

        res = re.search(r'.+знаки препинания[^.]*\.(.+)$', self.sentence, re.MULTILINE)
        if res is not None:
            self.sentence = self._to_line(res.group(1))

        parts = self.sentence.split('Цифры запишите')
        if len(parts) > 1:
            self.sentence = parts[0].strip()

        parts = self.sentence.split('Укажите цифр')
        if len(parts) > 1:
            self.sentence = parts[0].strip()

        self.sentence = self.sentence.replace(',', '__')
        for c in self.choices:
            self.sentence = self.sentence.replace(c['placeholder'], ',')

        self.sentence = self.sentence.replace(' ,', ',')
        self.mask: List[bool] = [m.group() == ',' for m in re.finditer(',|__', self.sentence)]
        self.sentence = self.sentence.replace('__', ',')

        self.labels: Optional[List[int]] = None
        if self.answer is not None:
            self.labels = [int(c['id'] in self.answer) for c in self.choices]
