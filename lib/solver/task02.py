import numpy as np
from lib.task import Task, Task02
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.speller import Speller

from typing import Optional, Any


class Task02Solver(BaseSolver):


    CANDIDATES = {
        'сочинительный союз': ['а', 'и', 'но', 'однако', 'тоже', 'также', 'зато', 'однако', 'или', 'либо'],
        'подчинительный союз': ['если', 'что', 'потому что', 'как', 'когда', 'чтобы'],
        'частицу': ['даже', 'только', 'именно'],
        'наречие': ['теперь', 'поэтому', 'отсюда', 'сначала', 'настолько'],
        'местоимение': ['это', 'эта', 'этот', 'эти', 'все'],
        'союзное слово': ['которой', 'которому', 'который', 'которым', 'которых'],
    }

    def __init__(self, bert: Optional[Bert] = None, speller: Optional[Speller] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

    def get_task_type(self) -> str:
        return Task.TYPE_02

    def solve(self, task: Task02) -> Any:
        if task.missed_text == '':
            return ''

        if task.candidates:
            word_candidates = task.candidates
        elif task.word_type in self.CANDIDATES:
            word_candidates = self.CANDIDATES[task.word_type]
        else:
            return self.solve_unknown(task)

        if '[SEP] [MASK]' in task.missed_text:
            word_candidates = [word[0].upper() + word[1:] for word in word_candidates]

        scores = []
        for candidate in word_candidates:
            scores.append(self.bert.get_word_in_text_scores(task.missed_text, candidate)[0])

        return word_candidates[np.argmax(scores)].replace(' ', '').lower()

    def solve_unknown(self, task: Task02) -> str:
        allowed_pos = {'CONJ', 'ADJF', 'ADVB', 'PRCL'}
        for word in self.bert.predict_masked_token(task.missed_text, num_words=30):
            if self.speller.parse_morph(word).tag.POS in allowed_pos:
                return word.lower()

        return ''
