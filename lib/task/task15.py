import re
from nltk.tokenize import word_tokenize
from lib.task.base import Task, MultipleChoiceTask
from typing import Dict, List


class Task15(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_15

        self.tokens: List[str] = get_tokens(self.text)
        self.positions: List[int] = [i for i, token in enumerate(self.tokens) if '__' in token]

        self.char: str = 'нн'
        match = re.search(r'пишется\s(н|нн)[^н]', self.text.lower())
        if match:
            self.char = match.group(1)


def get_tokens(text: str) -> List[str]:
    i = 1
    mark = f'({i})'
    words = []

    for word in text.split(' '):
        if mark in word:
            word = word.replace(mark, '__')
            i += 1
            mark = f'({i})'

        words.append(word)

    return word_tokenize(' '.join(words))
