import re
from lib.task.base import Task, ChoiceTask
from typing import Dict, List, Optional


class Task03(ChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_03

        parts = self.text.split('предложении текста')
        blacklist = [
            'Выпишите цифру',
            'Определите значение',
            'Прочитайте фрагмент',
            'Прочитайте текст',
            'в каком значении это слово',
        ]

        lines1 = self.get_numbered_lines(parts[0], blacklist)
        lines2 = self.get_numbered_lines(parts[1], blacklist)

        self.lines: List[str] = []
        if len(lines1) > len(lines2):
            self.lines = lines1
        else:
            self.lines = lines2

        question_text = self.remove_numbered_lines(self.lines)

        self.word: str = ''
        res = re.findall(r'значения слова (\w+)', question_text, re.UNICODE)
        if len(res) == 1:
            self.word = res[0].lower()

        self.line_num: Optional[int] = None
        res = re.findall(r'([1-9])\) предложении текста', question_text)
        if len(res) == 1:
            self.line_num = int(res[0]) - 1
