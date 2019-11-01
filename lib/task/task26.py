from lib.task.base import Task, MatchingTask
from typing import Dict


class Task26(MatchingTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_26

        lines = self.get_numbered_lines(blacklist=[
            'Прочитайте фрагмент рецензии',
            'Прочитайте текст',
            '.«',
        ])
        question_text = self.remove_numbered_lines(lines)
