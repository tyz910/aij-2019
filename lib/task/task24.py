from lib.task.base import Task, TextTask
from typing import Dict, List


class Task24(TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_24

        self.lines: List[str] = self.get_numbered_lines(blacklist=[
            'из предложений',
            'из предложения',
            'прочитайте текст'
        ])
        self.question_text: str = self.remove_numbered_lines(self.lines)
        self.lines[-1] = self.split_lines(self.lines[-1])[0]
