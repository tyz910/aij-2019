import numpy as np
from lib.task import Task, Task14
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.speller import Speller

from typing import Optional, Any, List, Tuple


class Task14Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None, speller: Optional[Speller] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

    def get_task_type(self) -> str:
        return Task.TYPE_14

    def solve(self, task: Task14) -> Any:
        lines = []
        line_word_pairs = []

        for line, word_pair in zip(task.lines, task.word_pairs):
            is_candidate = True
            for word_parts in word_pair:
                word_spelled = ''.join(word_parts)
                is_known = self.speller.is_known(word_spelled)

                if not is_known:
                    if word_parts[0] == 'полу':
                        is_known = True

                    if word_parts[0] == 'пол':
                        if self.speller.parse_morph(word_parts[1]).tag.POS == 'NOUN':
                            if word_parts[1] not in 'лаоиеёэыуюя':
                                is_known = True

                is_candidate = is_candidate and is_known

            if is_candidate:
                lines.append(line)
                line_word_pairs.append(word_pair)

        scores = []
        for line, word_pair in zip(lines, line_word_pairs):
            total_score = 0
            for word_parts in word_pair:
                word_spelled = ''.join(word_parts)
                word_spaced = ' '.join(word_parts)
                word_hyphen = ' '.join(word_parts)

                score_spaced = self.bert.get_replace_proba(line, word_spelled, word_spaced)
                score_hyphen = self.bert.get_replace_proba(line, word_spelled, word_hyphen)
                score = max(score_spaced, score_hyphen)
                if score > 1.0:
                    score = 1.0

                total_score += score

            scores.append(total_score)

        if scores:
            answer_idx = int(np.argmin(scores))
        else:
            answer_idx = 0
            line_word_pairs = task.word_pairs

        return ''.join([''.join(word_parts) for word_parts in line_word_pairs[answer_idx]])
