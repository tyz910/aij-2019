import numpy as np
from lib.task import Task, Task10, Task10Text, Task10MultipleChoice
from lib.solver.base import BaseSolver
from lib.util.speller import Speller
from lib.util.classifier import LgbClassifier
from sklearn.linear_model import LogisticRegression

from typing import Optional, Union, List, Dict, Tuple


class Task10Solver(BaseSolver):
    CHARS = ['а', 'о', 'е', 'и', 'у', 'ю', 'ы', 'я', 'с', 'з', 'т', 'д', 'ч', 'щ', 'ь', 'ъ', '']
    INVERSE_CHARS = {
        'а': {'о', 'у', 'ю', 'я'},
        'о': {'а', 'у', 'ю'},
        'е': {'и', 'о'},
        'и': {'е', 'ы'},
        'у': {'а', 'ю', 'я'},
        'ю': {'я', 'у', 'а'},
        'ы': {'и', 'о'},
        'я': {'ю', 'а', 'у'},
        'с': {'з'},
        'з': {'с'},
        'т': {'д'},
        'д': {'т'},
        'ч': {'щ'},
        'щ': {'ч'},
        'ь': {'', 'ъ'},
        'ъ': {'', 'ь'},
        '': {'ь', 'ъ'}
    }

    def __init__(self, speller: Optional[Speller] = None):
        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

        self.model: LgbClassifier = LgbClassifier('task10')
        self.model_linear = self.load_pkl('task10')
        if self.model_linear is None:
            self.model_linear = LogisticRegression(C=1.0)

        self.word_cache: Dict = {}

    def get_task_type(self) -> str:
        return Task.TYPE_10

    def solve(self, task: Task10) -> Union[str, List[str]]:
        if isinstance(task, Task10Text):
            if task.char is None:
                return self.solve_text_without_char(task)
            else:
                return self.solve_text_with_char(task)

        if isinstance(task, Task10MultipleChoice):
            if task.char is None:
                return self.solve_multiple_without_char(task)
            else:
                return self.solve_multiple_with_char(task)

        return None

    def solve_text_with_char(self, task: Task10Text) -> str:
        word_line_scores = []

        for word_line in task.word_lines:
            chars, scores = self.predict_chars_for_words(word_line)
            scores_by_char = {char: score for char, score in zip(chars, scores)}
            word_line_scores.append(scores_by_char[task.char])

        max_idx = int(np.argmax(word_line_scores))
        max_word_line = task.word_lines[max_idx]

        return ''.join([word.replace('..', task.char) for word in max_word_line])

    def solve_text_without_char(self, task: Task10Text) -> str:
        word_line_scores = []
        word_line_chars = []

        for word_line in task.word_lines:
            chars, scores = self.predict_chars_for_words(word_line)
            word_line_scores.append(scores[0])
            word_line_chars.append(chars[0])

        max_idx = int(np.argmax(word_line_scores))
        max_word_line = task.word_lines[max_idx]
        max_char = word_line_chars[max_idx]

        return ''.join([word.replace('..', max_char) for word in max_word_line])

    def solve_multiple_without_char(self, task: Task10MultipleChoice) -> List[str]:
        word_line_scores = []

        for word_line in task.word_lines:
            chars, scores = self.predict_chars_for_words(word_line)
            word_line_scores.append(scores[0])

        return [str(task.choices[idx]['id']) for idx in self.pick_idx(word_line_scores)]

    def solve_multiple_with_char(self, task: Task10MultipleChoice) -> List[str]:
        word_line_scores = []

        for word_line in task.word_lines:
            chars, scores = self.predict_chars_for_words(word_line)
            scores_by_char = {char: score for char, score in zip(chars, scores)}
            word_line_scores.append(scores_by_char[task.char])

        return [str(task.choices[idx]['id']) for idx in self.pick_idx(word_line_scores)]

    def pick_idx(self, word_line_scores: List[float]) -> List[int]:
        answer_idx = []

        word_line_scores = np.array(word_line_scores)
        sorted_idx = np.argsort(-word_line_scores)

        answer_idx.append(sorted_idx[0])
        sorted_idx = sorted_idx[1:]

        for idx in sorted_idx:
            if word_line_scores[idx] > 0.7:
                answer_idx.append(idx)

        return list(sorted(answer_idx))

    def train(self, tasks: List[Task10], save: bool = True):
        X, y = self.get_Xy_for_train()
        #self.model.train(X, y)
        self.model_linear.fit(X, y)

        if save:
            self.save_pkl('task10', self.model_linear)
            # self.model.save()

    def predict_chars_for_words(self, words: List[str]) -> Tuple[List[str], List[float]]:
        total_char_scores = {char: 0.0 for char in self.CHARS}

        for word in words:
            chars, scores = self.predict_chars(word)
            for char, score in zip(chars, scores):
                total_char_scores[char] += score

        chars = []
        scores = []
        for char, score in total_char_scores.items():
            chars.append(char)
            scores.append(score / len(words))

        scores = np.array(scores)
        idx = np.argsort(-scores)

        return np.array(chars)[idx].tolist(), scores[idx].tolist()

    def predict_chars(self, word: str) -> Tuple[List[str], List[float]]:
        scores = []
        for char in self.CHARS:
            # score = self.model_linear.predict([self.get_X(word, char, use_vocab=True)])[0][1]
            score = self.model_linear.predict_proba([self.get_X(word, char, use_vocab=True)])[0][1]
            scores.append(score)

        scores = np.array(scores)
        idx = np.argsort(-scores)

        return np.array(self.CHARS)[idx].tolist(), scores[idx].tolist()

    def get_Xy_for_train(self) -> Tuple[np.array, Optional[np.array]]:
        X = []
        y = []

        for word, chars in self.speller.examples.items():
            for char in chars:
                X.append(self.get_X(word, char))
                y.append(1)

                for inverse_char in self.INVERSE_CHARS[char]:
                    if inverse_char not in chars:
                        X.append(self.get_X(word, inverse_char))
                        y.append(0)

        return np.array(X), np.array(y)

    def get_X(self, word: str, char: str, use_vocab: bool = False) -> np.array:
        word = word.lower().replace('ё', 'е').strip()
        word_chars = self.get_word_chars(word)

        correct =int(word_chars[char]['correct'])
        known = int(word_chars[char]['known'])

        if use_vocab and self.speller.in_vocab(word.replace('..', char)):
            correct = known = 1

        features = [
            correct,
            known,
        ]

        total_correct = 0
        total_known = 0
        for c, info in word_chars.items():
            correct = int(info['correct'])
            known = int(info['known'])

            if use_vocab and self.speller.in_vocab(word.replace('..', c)):
                correct = known = 1

            total_correct += correct
            total_known += known

        features.append(total_correct)
        features.append(total_known)

        return np.array(features)

    def get_word_chars(self, word: str) -> Dict:
        if word not in self.word_cache:
            result = {}
            for char in self.CHARS:
                word_with_char = word.replace('..', char)
                result[char] = {
                    'correct': self.speller.is_correct(word_with_char),
                    'known': self.speller.is_known(word_with_char),
                }

            self.word_cache[word] = result

        return self.word_cache[word]
