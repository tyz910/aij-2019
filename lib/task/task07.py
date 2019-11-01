import re
from lib.task.base import Task, TextTask
from typing import Dict, List, Tuple


class Task07(TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_07

        self.lines: List[str] = []
        for line in self.split_lines():
            line = line.replace('ё', 'е').replace('Ё', 'Е').strip()

            if re.search(r'(допущена\sошибка|исправьте\sошибку|запишите\sисправленное)', line.lower()) is None:
                self.lines.append(line)
