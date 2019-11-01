import re
from nltk.util import ngrams
from lib.task import Task, Task06
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.speller import Speller
from lib.solver.sberbank import SberbankSolver

from typing import List, Dict, Any, Optional


class Task06Solver(BaseSolver):
    EXAMPLES = [
        ('биография жизни', 1),
        ('более исчерпывающий', 0),
        ('большая половина', 0),
        ('весёлый мажор', 0),
        ('взаимно помогать', 0),
        ('внутренний интерьер', 0),
        ('впервые дебютировать', 0),
        ('высокомерная спесь', 0),
        ('гипотетическое предположение', 0),
        ('главная суть', 0),
        ('глубокая бездна', 0),
        ('действительные реалии', 0),
        ('династия рода', 1),
        ('другая альтернатива', 0),
        ('жесты рук', 1),
        ('колючие тернии', 0),
        ('коренной абориген', 0),
        ('лаконичный краткий', 0),
        ('медицинская медсестра', 0),
        ('мемориальный памятник', 0),
        ('надменное высокомерие', 0),
        ('народный фольклор', 0),
        ('необычный экзотический', 0),
        ('новое будущее', 0),
        ('новая инициатива', 0),
        ('ноябрь месяц', 1),
        ('первая премьера', 0),
        ('основной лейтмотив', 0),
        ('отвлечённая абстракция', 0),
        ('открытие вернисажа', 1),
        ('отступить назад', 1),
        ('очень замечательный', 0),
        ('памятный сувенир', 0),
        ('первый дебют', 0),
        ('подлинный неподдельный', 1),
        ('подниматься вверх', 1),
        ('полностью завершить', 0),
        ('положительный успех', 0),
        ('правильное правописание', 0),
        ('прейскурант цен', 1),
        ('рублей денег', 1),
        ('свободная вакансия', 0),
        ('своя автобиография', 0),
        ('свой автопортрет', 0),
        ('секунд времени', 1),
        ('спускаться вниз', 1),
        ('сочетаться вместе', 1),
        ('столичный московский', 1),
        ('улыбнуться губами', 1),
        ('успешная победа', 0),
        ('холодный мороз', 0),
        ('хороший творческий', 0),
        ('хронометраж времени', 1),
        ('часа времени', 1),
        ('истинную правду', 0),
        ('чернеющей темноте', 0),
        ('самого начала', 0),
        ('свои индивидуальные', 0),
    ]

    def __init__(self, bert: Optional[Bert] = None, speller: Optional[Speller] = None, sberbank_solver: Optional[SberbankSolver] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

        if sberbank_solver is None:
            sberbank_solver = SberbankSolver()
        self.sberbank_solver: SberbankSolver = sberbank_solver

        self.embs = self.load_pkl('task06')

        self.pos_pairs = set()
        for text, word_idx in self.EXAMPLES:
            self.pos_pairs.add(self.get_pos_pair(text))

    def get_task_type(self) -> str:
        return Task.TYPE_06

    def solve(self, task: Task06) -> Any:
        if 'лишнее слово' not in task.text:
            return self.sberbank_solver.solve(task)

        best_s = None
        best_score = 0
        best_idx = 0

        for s in self.get_bigrams(task.sentence):
            score, idx = self.get_best_match(s)
            if score > best_score:
                best_score = score
                best_s = s
                best_idx = idx

        if best_s is not None:
            example = self.EXAMPLES[best_idx]
            return best_s.split(' ')[example[1]]
        else:
            return self.sberbank_solver.solve(task)

    def train(self, tasks: List[Task06], save: bool = True):
        self.embs = []
        for text, word_idx in self.EXAMPLES:
            self.embs.append(self.bert.eval(self.norm_text(text)))

        if save:
            self.save_pkl('task06', self.embs)

    def norm_text(self, text):
        return ' '.join([self.speller.parse_morph(word).normal_form for word in text.split(' ')])

    def get_pos_pair(self, text):
        pos_pairs = []
        for word in text.split(' '):
            pos = self.speller.parse_morph(word).tag.POS
            if pos == 'INFN':
                pos = 'VERB'

            pos_pairs.append(pos)

        return tuple(pos_pairs)

    def get_best_match(self, text):
        best_score = 0
        best_idx = 0

        emb = self.bert.eval(self.norm_text(text))
        for i, emb2 in enumerate(self.embs):
            score = emb.get_similarity(emb2)[-2]
            if score > best_score:
                best_score = score
                best_idx = i

        return best_score, best_idx

    def get_bigrams(self, text):
        words = re.sub(r'[^а-яё ]', '', text.lower()).split(' ')
        return [' '.join(w) for w in ngrams(words, 2)]
