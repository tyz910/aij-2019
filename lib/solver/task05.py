import os
import pickle
from lib.task import Task, Task05
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.speller import Speller

from typing import Optional, Any, Dict


class Task05Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None, speller: Optional[Speller] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

        model_dir = os.path.abspath(os.path.dirname(__file__) + '/../../var/model')
        with open(model_dir + '/paronyms.pickle', 'rb') as f:
            self.paronyms: Dict[str, str] = pickle.load(f)

    def get_task_type(self) -> str:
        return Task.TYPE_05

    def solve(self, task: Task05) -> Any:
        best_replace_proba = 0
        best_replace = ''

        for line, word in task.variants:
            word_morph = self.speller.parse_morph(word)
            if word_morph.normal_form in self.paronyms:
                paronym_word = self.speller.inflect_like(word, self.paronyms[word_morph.normal_form])
                replace_proba = self.bert.get_replace_proba(line, word, paronym_word)
                if replace_proba > best_replace_proba:
                    best_replace_proba = replace_proba
                    best_replace = paronym_word

        return best_replace
