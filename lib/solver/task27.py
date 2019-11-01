import re
import numpy as np
from summa import summarizer
from lib.task import Task, Task27
from lib.solver.base import BaseSolver
from lib.solver.sberbank import SberbankSolver
from lib.util.esse import EsseLoader, Esse
from lib.util.ner import NER
from lib.util.syntax import SyntaxParser
from nltk import sent_tokenize

from typing import Optional, Any, List


class Task27Solver(BaseSolver):
    def __init__(
        self,
        esse: Optional[EsseLoader] = None,
        ner: Optional[NER] = None,
        sberbank_solver: Optional[SberbankSolver] = None,
        syntax: Optional[SyntaxParser] = None
    ):
        if ner is None:
            ner = NER()
        self.ner: NER = ner

        if esse is None:
            esse = EsseLoader()
        self.esse: EsseLoader = esse

        if sberbank_solver is None:
            sberbank_solver = SberbankSolver()
        self.sberbank_solver: SberbankSolver = sberbank_solver

        if syntax is None:
            syntax = SyntaxParser()
        self.syntax: SyntaxParser = syntax

    def get_task_type(self) -> str:
        return Task.TYPE_27

    def solve(self, task: Task27) -> Any:
        author_name = self.get_author_name(task)
        esse_text = self.generate_esse(task.lines, author_name)

        if len(esse_text.split(' ')) < 150:
            return self.solve_sberbank(task)
        else:
            return esse_text

    def generate_esse(self, lines: List[str], author_name: str) -> str:
        text = ' '.join(lines)
        short_text = summarizer.summarize(text)

        esse = self.esse.make_esse(short_text)

        position_quote = self.get_position_quote(esse.position1, lines)
        reference_quote = self.get_reference_quote(esse.problem, position_quote, lines)

        problem_text = self.get_problem_text(esse.problem, author_name)
        position_text = self.get_position(esse.position1, esse.position2, position_quote)
        examples_text = self.get_examples_text(esse.examples)
        conclusion_text = self.get_conclusion_text(esse.conclusion)
        reference_text = self.get_reference_text(esse.problem, text, short_text, reference_quote)

        return f'{problem_text} {reference_text}\n\n{position_text}\n\n{examples_text}\n\n{conclusion_text}.'

    def solve_sberbank(self, task: Task27) -> Any:
        return self.sberbank_solver.ai.solvers[26].predict_from_model({
            'text': task.text,
        })

    def get_position_quote(self, position: str, lines: List[str]) -> str:
        best_line = ''
        best_score = 0

        for i, line in enumerate(lines):
            if i < len(lines) - 1:
                double_line = line + ' ' + lines[i + 1]
                if (200 > len(double_line) > 70) and '«' not in double_line and '»' not in double_line:
                    score = self.esse.sentence_encoder.get_similarity(position, double_line) ** 2
                    if score > best_score:
                        best_score = score
                        best_line = double_line

            if (200 > len(line) > 70) and '«' not in line and '»' not in line:
                score = self.esse.sentence_encoder.get_similarity(position, line) ** 2
                if score > best_score:
                    best_score = score
                    best_line = line

        return best_line

    def get_reference_quote(self, problem: str, position_quote: str, lines: List[str]) -> str:
        best_line = ''
        best_score = 0

        for i, line in enumerate(lines):
            if line in position_quote:
                continue

            if i < len(lines) - 1:
                double_line = line + ' ' + lines[i + 1]
                if (150 > len(double_line) > 30) and '«' not in double_line and '»' not in double_line:
                    score = self.esse.sentence_encoder.get_similarity(problem, double_line) ** 2
                    if score > best_score:
                        best_score = score
                        best_line = double_line

            if (150 > len(line) > 30) and '«' not in line and '»' not in line:
                score = self.esse.sentence_encoder.get_similarity(problem, line) ** 2
                if score > best_score:
                    best_score = score
                    best_line = line

        return best_line

    def get_position(self, position1: str, position2: str, position_quote: str) -> str:
        position_text = f'Позиция автора в данном тексте такова: {position1}.'

        if position_quote != '':
            position_text += f' Эта позиция прослеживается в отрывке: «{position_quote}».'

        if position2 != '':
            position_text += f' Я полностью согласен с мнением автора: {position2}.'
        else:
            position_text += f' Я полностью согласен с мнением автора.'

        return position_text

    def get_reference_text(self, problem, text, short_text, reference_quote) -> str:
        names = self.get_top_names(text)
        if len(names) > 1:
            name = names[0]
            name_morph = self.syntax.speller.parse_morph(name)
            name_cased = name_morph.inflect({'loct'}).word

            if name[0].isupper() or 'Name' in name_morph.tag or 'Surn' in name_morph.tag:
                name_cased = name_cased[0].upper() + name_cased[1:]

            start = 'Для того чтобы полнее раскрыть данную проблему, автор рассказывает о ' + name_cased
        else:
            start = 'Для того чтобы полнее раскрыть данную проблему, автор рассказывает'

        retries = 0
        while True:
            gen_text = self.complete_text(short_text + ' ' + problem + ' ' + start)
            num_sent = len(sent_tokenize(gen_text))
            if ('xxbos' in gen_text or num_sent < 3) and retries < 3:
                retries += 1
                continue

            break

        text = start + ' ' + ' '.join(sent_tokenize(gen_text)[:2])

        if reference_quote != '':
            ref = f' Чувствуется заинтересованность автора в поднятой им проблеме: «{reference_quote}».'
        else:
            ref = ''

        retries = 0
        while True:
            gen_text2 = self.complete_text(problem + '. ' + ref)
            num_sent = len(sent_tokenize(gen_text2))
            if ('xxbos' in gen_text or num_sent < 3) and retries < 3:
                retries += 1
                continue

            break

        return text + ref + ' ' + ' '.join(sent_tokenize(gen_text2)[:2])

    @staticmethod
    def get_problem_text(problem: str, author_name: str) -> str:
        problem = problem.capitalize()
        return f'{problem} – вот проблема, над которой размышляет {author_name}.'

    @staticmethod
    def get_conclusion_text(conclusion: str) -> str:
        return f'Таким образом, могу сделать вывод, что {conclusion}'

    @staticmethod
    def get_examples_text(examples: List[str]):
        if len(examples) == 0:
            return ''

        examples_text = 'В подтверждение своих слов приведу примеры из художественной литературы. '
        examples_text += ' '.join(examples[:2])

        return examples_text

    def get_author_name(self, task: Task27) -> str:
        if task.author == '':
            return 'автор'

        author_name = self.ner.get_name(task.author)
        if len(author_name.split(' ')) < 3:
            author_name = 'автор'

        return author_name

    def get_top_names(self, text):
        nsubjs = {}
        next_sents = {}

        for sent in sent_tokenize(text):
            syntax = self.syntax.get_syntax(sent)
            for node in syntax.nodes:
                if node.link is None:
                    for node2 in syntax.nodes:
                        if node2.link == node.id and node2.link_type == 'nsubj':

                            if 'Tense=Past' in node.morph:
                                next_sents[node2.normal_form] = sent

                            if node2.normal_form not in nsubjs:
                                nsubjs[node2.normal_form] = 0
                            nsubjs[node2.normal_form] += 1

        scores = []
        names = []

        max_upper_idx = -1
        max_upper_score = 0

        idx = 0
        for name, score in nsubjs.items():
            morph = self.syntax.speller.parse_morph(name)
            if morph.tag.POS not in {'NOUN'}:
                continue

            names.append(name)
            scores.append(score)

            if 'Name' in morph.tag:
                if score > max_upper_score:
                    max_upper_score = score
                    max_upper_idx = idx

            idx += 1

        if max_upper_idx != -1:
            scores[max_upper_idx] += 100

        top_names_idx = np.argsort(-np.array(scores))[:3]
        return np.array(names)[top_names_idx]

    def complete_text(self, seed, n_words=100, temperature=0.9):
        text = self.sberbank_solver.ai.solvers[26].learn.predict(seed, n_words=n_words, no_unk=True, temperature=temperature)
        return self.clear_text(text[len(seed):])

    def clear_text(self, text):
        text = re.sub("[\t\r]+", "", text)
        text = re.sub("[ ]+[:]", ":", re.sub("[ ]+[.]", ".", re.sub("[«][ ]+", "«", re.sub("[ ]+[»]", "»", re.sub("[ ]+[,]", ",", re.sub("[ ]+", " ", text))))))
        text = re.sub("[ ]+[?]", "?", text)
        text = re.sub("[ ]+[!]", "!", text)
        text = re.sub("\n+", "\n", text)
        text = [line.strip() for line in text.split("\n")]
        text = "\n".join(text)

        return text.replace("\n", " ")

