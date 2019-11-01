from lib.task import Task, Task15
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.speller import Speller

from typing import List, Optional


class Task15Solver(BaseSolver):
    INVERSE_CHARS = {
        'н': 'нн',
        'нн': 'н',
    }

    def __init__(self, bert: Optional[Bert] = None, speller: Optional[Speller] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

    def get_task_type(self) -> str:
        return Task.TYPE_15

    def solve(self, task: Task15) -> List[str]:
        answer = []
        chars = []
        unknown = []
        tokens = task.tokens[:]

        inverse_char = self.INVERSE_CHARS[task.char]

        for i, pos in enumerate(task.positions):
            word = tokens[pos]
            word_with_char = word.replace('__', task.char)
            word_with_inverse_char = word.replace('__', inverse_char)

            known_with_char = self.speller.is_known(word_with_char)
            known_with_inverse_char = self.speller.is_known(word_with_inverse_char)

            if known_with_char and not known_with_inverse_char:
                chars.append(task.char)
                answer.append(str(i + 1))
                tokens[pos] = tokens[pos].replace('__', task.char)
            elif known_with_inverse_char and not known_with_char:
                chars.append(inverse_char)
                tokens[pos] = tokens[pos].replace('__', inverse_char)
            else:
                unknown.append((str(i + 1), pos))

        for a, pos in unknown:
            word = tokens[pos]
            word_with_char = word.replace('__', task.char)
            word_with_inverse_char = word.replace('__', inverse_char)

            tokens[pos] = word_with_char
            text = ' '.join(tokens).replace('__', task.char)
            for line in task.split_lines(text):
                if word_with_char in line:
                    text = line
                    break

            replace_proba = self.bert.get_replace_proba(text, word_with_char, word_with_inverse_char)
            if replace_proba < 1.0:
                answer.append(a)
            else:
                tokens[pos] = word_with_inverse_char

        return list(sorted(answer))
