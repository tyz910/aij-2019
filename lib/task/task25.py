import re
from lib.task.base import Task, MultipleChoiceTask

from typing import Dict, List, Optional, Tuple


class Task25(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_25

        self.lines: List[str] = self.get_numbered_lines(blacklist=[
            'среди предложений',
            'прочитайте текст',
        ])
        self.question_text: str = self.remove_numbered_lines(self.lines)

        last_parts = self.split_lines(self.lines[-1])
        self.lines[-1] = last_parts[0]
        if len(last_parts) > 1:
            self.question_text += ' '.join(last_parts[1:])

        self.line_range: Optional[Tuple[int, int]] = None
        search_range = re.findall(r'предложений\s([0-9]{1,2})[-–−—]([0-9]{1,2})', self.question_text)
        if len(search_range) == 1:
            self.line_range = (int(search_range[0][0]), int(search_range[0][1]))

        self.connection_features: List[int] = [
            int('личного' in self.question_text),
            int('притяжательного' in self.question_text),
            int('указательного' in self.question_text),
            int('определительного' in self.question_text),
            int('местоимения' in self.question_text or 'местоимений' in self.question_text),
            int('местоименного' in self.question_text),
            int('наречия' in self.question_text),
            int('усилительной' in self.question_text),
            int('указательной' in self.question_text),
            int('частицы' in self.question_text),
            int('однокоренных' in self.question_text),
            int('форм' in self.question_text),
            int('противительного' in self.question_text),
            int('сочинительного' in self.question_text),
            int('союза' in self.question_text),
            int('лексического повтора' in self.question_text),
            int('синоним' in self.question_text),
        ]

        self.line_pairs: List[Tuple[str, str]] = []
        if self.line_range is not None and len(self.lines) >= self.line_range[1]:
            for i in range(self.line_range[0] - 1, self.line_range[1]):
                self.line_pairs.append((self.lines[i - 1], self.lines[i]))

        if self.answer:
            if len(self.answer) > 1:
                fixed_answer = []

                if 'Мой отец и исправник были поражены' in self.text:
                    return

                while len(self.answer) > 0:
                    if int(self.answer[0]) < self.line_range[1]:
                        fixed_answer.append(''.join(self.answer[:2]))
                        self.answer = self.answer[2:]
                    else:
                        fixed_answer.append(self.answer[0])
                        self.answer = self.answer[1:]

                self.answer = fixed_answer
