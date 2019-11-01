import re
from lib.task.base import Task, TextTask
from typing import Dict, List, Tuple


class Task05(TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_05

        self.variants: List[Tuple[str, str]] = []
        for line in self.split_lines():
            cap_words = re.findall(r'[А-ЯЁ]{3,}', line)
            if len(cap_words) == 1 and 'НЕВЕРНО' not in cap_words:
                cap_word = cap_words[0]
                self.variants.append((line.replace(cap_word, cap_word.lower()), cap_word.lower()))
