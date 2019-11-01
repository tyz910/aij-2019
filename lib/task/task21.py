from lib.task.base import Task, MultipleChoiceTask
from typing import Dict, List, Optional


class Task21(MultipleChoiceTask):
    def __init__(self, data: Dict):
        data['text'] = data['text'].replace('—', '–')
        super().__init__(data)
        self.type = Task.TYPE_21

        self.lines: List[str] = self.get_numbered_lines(blacklist=[
            'Запишите',
            'Найдите',
        ])
        self.question_text: str = self.remove_numbered_lines(self.lines)

        self.question_type: Optional[str] = None

        if 'в которых тире' in self.question_text:
            self.question_type = '–'

        if 'в которых запятая' in self.question_text or 'в которых запятые' in self.question_text:
            self.question_type = ','

        if 'в которых двоеточие' in self.question_text:
            self.question_type = ':'
