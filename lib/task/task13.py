import re
from lib.task.base import Task, TextTask

from typing import Dict, List, Tuple


class Task13(TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_13

        self.words: List[Tuple[str, str]] = []
        self.lines: List[str] = []

        for line in self.split_lines():
            if 'пишется слитно' in line:
                continue

            if '(не)' in line.lower() or '(ни)' in line.lower():
                match = re.search(r'\((Н[ЕИ])\)([А-ЯЁ]+)', line, re.IGNORECASE)
                if match:
                    self.lines.append(line.replace(match.group(0), '[MASK]'))

                    part1 = match.group(1).lower()
                    part2 = match.group(2).lower()
                    self.words.append((part1 + part2, part1 + ' ' + part2))
