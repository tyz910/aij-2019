import re
from lib.task.base import Task, TextTask

from typing import Dict, List, Tuple


class Task27(TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_27

        self.author: str = ''
        self.lines = self.get_numbered_lines(blacklist=[
            'Прочитайте текст',
            'Напишите сочинение'
        ])

        last = self.lines[-1]
        parts = re.split(r'\([пП]о\s[^)]+\)', last)
        if len(parts) > 1:
            self.lines[-1] = parts[0]
            self.author = parts[1]
        else:
            parts = self.split_lines(last)
            if len(parts) > 1:
                self.lines[-1] = parts[0]
                self.author = ' '.join(parts[1:])
            else:
                self.lines = self.lines[:-1]
                self.author = last

        self.author = self.author.replace('*', '').strip()
