from lib.task.base import Task, TextTask
from typing import Dict, List, Tuple


class Task04(TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_04

        self.words: List[Tuple[str, int]] = []
        for line in self.text.split('\n'):
            line = line.strip()
            if len(line.split(' ')) == 1:
                stresses = [i for i, c in enumerate(line) if c.isupper()]
                if len(stresses) == 1:
                    self.words.append((line.lower(), stresses[0]))
