import numpy as np
from lib.task import Task, Task25
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.speller import Speller
from lib.util.classifier import LgbClassifier, CtbClassifier
from nltk.tokenize import word_tokenize

from typing import List, Optional, Any, Tuple


class Task25Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None, speller: Optional[Speller] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

        # self.model = LgbClassifier('task25')
        self.model = CtbClassifier('task25')

    def get_task_type(self) -> str:
        return Task.TYPE_25

    def solve(self, task: Task25) -> Any:
        X, _ = self.get_Xy([task])
        preds = self.model.predict(X)[:, 1]

        preds_sorted = np.argsort(-preds)
        variants = list(range(task.line_range[0], task.line_range[1] + 1))

        answer = [
            str(variants[preds_sorted[0]]),
        ]

        return answer

    def train(self, tasks: List[Task25], save: bool = True):
        X, y = self.get_Xy(tasks)
        self.model.train(X, y)

        if save:
            self.model.save()

    def get_Xy(self, tasks: List[Task25]) -> Tuple[np.array, Optional[np.array]]:
        X = []
        y = []

        for task in tasks:
            num = task.line_range[0]
            for line_a, line_b in task.line_pairs:
                emb1 = self.bert.eval(line_a, line_b)
                # emb2 = self.bert.eval(line_b)

                X.append(np.concatenate((
                    task.connection_features,
                    # emb1.get_clf_output(),
                    emb1.get_sentence_embeddings()[-1:].flatten(),
                    # emb2.get_sentence_embeddings()[-1:].flatten(),
                    np.array([
                        # self.get_words_intersection(line_a, line_b, task.question_text),
                        *self.check_pronoun(line_b, task.question_text),
                        self.check_advb(line_b, task.question_text),
                        self.check_conj(line_b, task.question_text),
                        self.check_prcl(line_b, task.question_text),
                    ])
                )))

                if y is not None and task.answer is not None:
                    y.append(int(str(num) in task.answer))
                else:
                    y = None

                num += 1

        if y is not None:
            y = np.array(y)

        return np.array(X), y

    def get_words(self, text, pos_blacklist):
        words = set()

        for word in word_tokenize(text):
            morph = self.speller.parse_morph(word)

            pos_in_bl = False
            for pos in pos_blacklist:
                if pos in morph.tag:
                    pos_in_bl = True
                    break

            if pos_in_bl:
                continue

            words.add(morph.normal_form)

        return words

    def get_words_intersection(self, line1, line2, question_text):
        if 'лексического повтора' not in question_text:
            return 0

        pos_blacklist = ['PNCT', 'PRCL', 'CONJ', 'PREP']
        words1 = self.get_words(line1, pos_blacklist)
        words2 = self.get_words(line2, pos_blacklist)

        common_words = words1 & words2
        return len(common_words)

    def check_pronoun(self, text, question_text):
        has_pronoun = 0
        match_pronoun_type = 0

        PRONOUNS = {
            'личного': {'я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они'},
            'притяжательного': {'мой', 'твой', 'ваш', 'наш', 'свой', 'его', 'ее', 'их'},
            'указательного': {'это', 'тот', 'этот', 'такой', 'таков', 'столько'},
            'определительного': {'весь', 'всякий', 'каждый', 'сам', 'самый', 'иной', 'другой'},
        }

        total_types = 0
        matched_types = 0

        if 'местоимения' in question_text or 'местоимений' in question_text:
            words = {word.replace('ё', 'е').lower() for word in word_tokenize(text)}
            words |= {self.speller.parse_morph(word).normal_form for word in words}

            for pronoun_type, pronouns in PRONOUNS.items():
                has_pronoun = max(has_pronoun, int(len(words & pronouns) > 0))
                if pronoun_type in question_text:
                    total_types += 1
                    matched_types += int(len(words & pronouns) > 0)

        if total_types > 0:
            match_pronoun_type = matched_types / total_types

        return has_pronoun, match_pronoun_type

    def check_advb(self, text, question_text):
        has_advb = 0

        ADVERBS = {'здесь', 'там', 'тут', 'туда', 'так', 'оттуда', 'тогда', 'затем', 'оттого', 'потому', 'поэтому',
                   'где', 'куда', 'когда', 'зачем', 'как', 'почему', 'откуда', 'отчего'}

        if 'наречия' in question_text:
            words = {word.lower() for word in word_tokenize(text)}
            words |= {self.speller.parse_morph(word).normal_form for word in words}
            has_advb = int(len(words & ADVERBS) > 0)

        return has_advb

    def check_conj(self, text, question_text):
        if 'союза' in question_text:
            first_word = word_tokenize(text)[0]
            return int(self.speller.parse_morph(first_word).tag.POS == 'CONJ')

        return 0

    def check_prcl(self, text, question_text):
        score = 0.0

        if 'частицы' in question_text:
            words = word_tokenize(text)[:2]
            first_word = self.speller.parse_morph(words[0])

            if first_word.tag.POS == 'PRCL':
                score = 1.0

            if first_word.tag.POS == 'CONJ':
                score = 0.5

            if words[1] == 'ведь':
                score = 1.0

        return score
