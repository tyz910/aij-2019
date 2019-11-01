import re
from lib.task.base import Task, TextTask
from typing import Dict, List, Tuple


class Task14(TextTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_14

        self.lines: List[str] = []
        self.word_pairs: List[Tuple[List[str, ...], ...]] = []

        for line in self.split_lines():
            words = re.findall(r'([А-ЯЁ()]{5,})', line)
            if len(words) != 2:
                continue

            word_pair = tuple(re.sub(r'[()]', ' ', w.lower()).split() for w in words)
            self.word_pairs.append(word_pair)

            for word, word_parts in zip(words, word_pair):
                line = line.replace(word, ''.join(word_parts))
            self.lines.append(line)
