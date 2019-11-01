import re
from lib.task.base import Task, TextTask, MultipleChoiceTask
from typing import Dict, List, Optional


class Task10(Task):
    def __init__(self, data: Dict):
        data['text'] = self._fix_dots(data['text'])
        super().__init__(data)
        self.type = Task.TYPE_10

        self.char: Optional[str] = None
        self.word_lines: List[List[str]] = []

    @staticmethod
    def _fix_dots(s: str) -> str:
        return s.replace('…', '..').replace('‥', '..')

    def _set_question_details(self, question_text: str, lines: List[str]):
        for line in lines:
            words = re.findall(r'[а-яё]*\.{2,}[а-яё]*', line.lower())
            if len(words) > 0:
                self.word_lines.append(words)

        result = re.findall(r'буква ([эоуаыеёюяи])', question_text.lower())
        if len(result) == 1:
            self.char = result[0]


class Task10Text(Task10, TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)

        question_text: str = ''
        lines: List[str] = []

        for line in self.text.split('\n'):
            if '..' in line:
                lines.append(line)
            else:
                question_text += ' ' + line

        self._set_question_details(question_text, lines)


class Task10MultipleChoice(Task10, MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)

        self._set_question_details(self.text, [self._fix_dots(c['text']) for c in self.choices])
