import re
from lib.task.base import Task, TextTask
from typing import Dict, List, Tuple


class Task06(TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_06

        self.sentence: str = ''
        for line in self.split_lines():
            if re.match(r'.*(отредактируйте|выпишите|запишите|исправьте|исключите).*', line.lower()):
                continue

            self.sentence += line
