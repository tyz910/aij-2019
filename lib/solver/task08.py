import re
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from lib.task import Task, Task08
from lib.solver.base import BaseSolver
from lib.util.bert import Bert
from lib.util.speller import Speller
from lib.util.syntax import SyntaxParser
from lib.util.classifier import CtbClassifier
from lib.sberbank.utils import sber_encode, sber_decode

from typing import List, Dict, Tuple, Optional


class Task08Solver(BaseSolver):
    def __init__(self, bert: Optional[Bert] = None, speller: Optional[Speller] = None, syntax: Optional[SyntaxParser] = None):
        if bert is None:
            bert = Bert()
        self.bert: Bert = bert

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

        if syntax is None:
            syntax = SyntaxParser(self.speller)
        self.syntax: SyntaxParser = syntax

        self.model = CtbClassifier('task08')

    def get_task_type(self) -> str:
        return Task.TYPE_08

    def solve(self, task: Task08) -> Dict[str, str]:
        df = self.get_preds_df(task)

        return self.preds_df_to_answer(task, df)

    def get_preds_df(self, task: Task08):
        X, _ = self.get_Xy([task])
        preds = self.model.predict(X)

        left_ids = []
        left_labels = []

        for left_id, label in task.left_labels.items():
            left_ids.append(left_id)
            left_labels.append(label)

        return pd.DataFrame(preds[:, left_labels], columns=left_ids, index=[c['id'] for c in task.choices])

    def get_hard_answers(self, task):
        answer = {}

        for i, c in enumerate(task.choices):
            text_id = str(i+1)
            text = c['text']

            if self.match1(text):
                answer[text_id] = 1

        return answer

    def match1(self, text):
        if self.prep_po(text) > 0:
            return True

        elif self.prep_case(text) > 0:
            return True

        return False

    def preds_df_to_answer(self, task, df) -> Dict[str, str]:
        answer = {}

        # hard_answer = self.get_hard_answers(task)
        # class_id_labels = {v: k for k, v in task.left_labels.items()}
        # for text_id, class_id in hard_answer.items():
        #     if class_id in class_id_labels:
        #         label = class_id_labels[class_id]
        #         answer[label] = text_id
        #         df = df.drop(text_id, axis=0).drop(label, axis=1)
        #     else:
        #         df = df.drop(text_id, axis=0)

        while len(df.columns) > 0:
            max_column = df.max().idxmax()
            df, answer = self.pick_label(df, max_column, answer)

        return answer

    def pick_label(self, df: pd.DataFrame, max_column: str, answer: Dict[str, str]) \
            -> Tuple[pd.DataFrame, Dict[str, str]]:
        max_choice = df[max_column].idxmax()
        answer[max_column] = max_choice
        df = df.drop(max_choice, axis=0).drop(max_column, axis=1)
        return df, answer

    def train(self, tasks: List[Task08], save: bool = True):
        X, y = self.get_Xy(tasks, is_train=True)

        unq, idx = np.unique(X, axis=0, return_index=True)
        X = X[idx]
        y = y[idx]

        self.model.train(X, y, num_class=len(Task08.CLASSES))

        if save:
            self.model.save()

    def get_features(self, text):
        emb = self.bert.eval(text)

        return np.concatenate((
            emb.get_sentence_embeddings()[-4:].flatten(),
            np.array([
                self.starts_with_grnd(text),
                self.prep_po(text),
                self.prep_case(text),
                self.title_case(text),
                self.talk_word(text),
                *self.verb_forms(text),
                self.has_comma(text),
                *self.has_prtf(text),
                self.has_quote(text),
                self.has_and(text),
                self.has_not_only(text),
                *self.chto_li(text),
                self.multiple_sent(text),
                self.chto_ya(text),
                *self.get_number_gender_changed(text),
                *self.conj_mismatch(text),
            ]),
        ))

    def get_Xy_for_train(self, tasks: List[Task08], label_idx):
        X = []
        y = []

        for task in tasks:
            answer = {v: k for k, v in task.answer.items()}
            if label_idx in task.left_labels.values():
                for choice in task.choices:
                    if choice['id'] in answer:
                        label = task.left_labels[answer[choice['id']]]
                        label = int(label == label_idx)
                    else:
                        label = 0

                    X.append(self.get_features(choice['text']))
                    y.append(label)

        return np.array(X), np.array(y)

    def get_Xy(self, tasks: List[Task08], is_train: bool = False) -> Tuple[np.array, Optional[np.array]]:
        X = []
        y = []

        for task in tasks:
            if task.answer is not None:
                answer = {v: k for k, v in task.answer.items()}
            else:
                answer = None

            for choice in task.choices:
                if is_train and choice['id'] not in answer:
                    continue

                X.append(self.get_features(choice['text']))

                if y is not None and answer is not None:
                    if choice['id'] in answer:
                        y.append(task.left_labels[answer[choice['id']]])
                    else:
                        y = None
                        # y.append(10)
                else:
                    y = None

        if y is not None:
            y = np.array(y)

        return np.array(X), y

    def starts_with_grnd(self, text):
        if ',' in text:
            for word in text.split(',')[0].split(' '):
                # GRND - деепричастие
                if self.speller.parse_morph(word).tag.POS == 'GRND':
                    return 1

        return 0

    def prep_po(self, text):
        match_po = False

        for word in word_tokenize(text.lower()):
            if word == 'по':
                match_po = True
                continue

            if match_po:
                if word in ['приезду', 'прилёту', 'прилету']:
                    return 1

                if word.endswith('ию') and word not in ['отношению', 'мнению']:
                    return 1

            match_po = False

        return 0

    def prep_case(self, text):
        prep_cases = {
            'благодаря': 'datv',
            'сродни': 'datv',
            'подобно': 'datv',
            'вопреки': 'datv',
            'навстречу': 'datv',
            'вслед': 'datv',
            'наперерез': 'datv',
            'наперекор': 'datv',
            'согласно': 'datv',
            'взамен': 'gent',

            'вблизи': 'gent',
            'ввиду': 'gent',
            'вглубь': 'gent',
            'вдоль': 'gent',
            'вместо': 'gent',
            'вне': 'gent',
            'внутрь': 'gent',
            'возле': 'gent',
            'вследствие': 'gent',
            'средь': 'gent',
            'среди': 'gent',
            'напротив': 'gent',
            'посредством': 'gent',
            'посредине': 'gent',
            'посреди': 'gent',
            'после': 'gent',
            'помимо': 'gent',
            'около': 'gent',
            'кроме': 'gent',
            'наподобие': 'gent',
        }

        syntax = self.syntax.get_syntax(text)
        for i, node in enumerate(syntax.nodes):
            if node.normal_form in prep_cases:
                if node.link_type in {'case', 'advmod'} and syntax.nodes[i+1].link_type not in {'case', 'advmod'}:
                    node2 = node.get_link()
                    case = node2.morph2.tag.case
                    if case is not None:
                        if case != prep_cases[node.normal_form]:
                            word = node2.morph2.word
                            word2 = node2.morph2.inflect({prep_cases[node.normal_form]}).word

                            if word != word2:
                                return 1

        return 0

    def title_case(self, text):
        for line in re.findall(r'«([^»]+)»', text):
            before = word_tokenize(text.split('«' + line)[0])
            if len(before) > 0:
                word_before = before[-1]
                prep_before = self.speller.parse_morph(word_before).tag.POS == 'PREP'
            else:
                prep_before = False

            if line[0].isupper():
                words = word_tokenize(line)
                if len(words) <= 5:
                    for word in words:
                        case = self.speller.parse_morph(word).tag.case
                        if case is not None:
                            if prep_before and case == 'nomn':
                                return 1

                            if not prep_before and case != 'nomn':
                                return 1

                            break

        return 0

    def talk_word(self, text):
        for word in word_tokenize(text):
            if self.speller.parse_morph(word).normal_form in ['говорить', 'спросить', 'сказать']:
                return 1

        return 0

    def verb_forms(self, text):
        tenses = set()
        aspects = set()

        for word in word_tokenize(text):
            tag = self.speller.parse_morph(word).tag
            if tag.POS == 'VERB':
                tenses.add(tag.tense)
                aspects.add(tag.aspect)

        return len(tenses), len(aspects)

    def has_comma(self, text):
        return int(',' in text)

    def has_quote(self, text):
        return int('«' in text)

    def has_prtf(self, text):
        tags = []
        for word in word_tokenize(text):
            tag = self.speller.parse_morph(word).tag
            tags.append(tag)
            # PRTF - причастие
            if tag.POS == 'PRTF':
                case_fail = 0
                if len(tags) > 2 and 'PNCT' in tags[-2] and 'NOUN' in tags[-3]:
                    case_fail = int(tags[-3].case != tag.case)

                return 1, case_fail

        return 0, 0

    def has_and(self, text):
        return int(' и ' in text or 'не только' in text.lower() or 'не столько' in text.lower())

    def has_not_only(self, text):
        return int('не только' in text.lower() or 'не столько' in text.lower())

    def chto_li(self, text):
        return int(' что ' in text), int(' ли ' in text)

    def multiple_sent(self, text):
        text = re.sub(r'(\.)(\w\.)', r'\1 \2', text)
        return int(len(sent_tokenize(text)) > 1)

    def chto_ya(self, text):
        return int(re.search(r'что\s.*[я|]\s', text) is not None)

    def get_number_gender_changed(self, text):
        number_changed = 0
        gender_changed = 0

        for first, second in self.get_nsubj_pair(text):
            first_tag = self.speller.parse_morph(first[1]).tag
            second_tag = self.speller.parse_morph(second[1]).tag

            first_match = re.search(r'Number=(Sing|Plur)', first[5])
            second_match = re.search(r'Number=(Sing|Plur)', second[5])
            if first_match is not None and second_match is not None:
                if first_match.group(1) != second_match.group(1):
                    number_changed += 1

            first_match = re.search(r'Gender=(Fem|Masc|Neut)', first[5])
            second_match = re.search(r'Gender=(Fem|Masc|Neut)', second[5])
            if first_match is not None and second_match is not None:
                if first_match.group(1) != second_match.group(1):
                    gender_changed += 1

            if first[3] not in {'NOUN', 'NPRO'}:
                continue

            if second_tag.POS not in {'VERB', 'PRTS'}:
                continue

            if 'nomn' not in first_tag:
                continue

            if first_tag.number is not None and second_tag.number is not None and first_tag.number != second_tag.number:
                number_changed += 1

            if first_tag.gender is not None and second_tag.gender is not None and first_tag.gender != second_tag.gender:
                gender_changed += 1

        return number_changed, gender_changed

    def conj_mismatch(self, text):
        pos_mismatch = 0
        voice_mismatch = 0

        for first, second in self.get_and_conj_pair(text):
            first_tag = self.speller.parse_morph(first[1]).tag
            second_tag = self.speller.parse_morph(second[1]).tag

            if first[3] != second[3]:
                pos_mismatch += 1

            if first_tag.POS != second_tag.POS:
                pos_mismatch += 1

            first_match = re.search(r'Voice=([A-Za-z]+)', first[5])
            second_match = re.search(r'Voice=([A-Za-z]+)', second[5])
            if first_match is not None and second_match is not None:
                if first_match.group(1) != second_match.group(1):
                    voice_mismatch += 1

        return pos_mismatch, voice_mismatch

    def get_syntax(self, text):
        processed = self.syntax.process_pipeline.process(sber_encode(text))
        content = [l for l in sber_decode(processed).split('\n') if not l.startswith('#')]
        tagged = [w.split('\t') for w in content if w]
        return tagged

    def get_nsubj_pair(self, text):
        syntax = self.get_syntax(text)

        pairs = []
        for syn in syntax:
            ref = int(syn[6]) - 1
            if 'nsubj' in syn[7]:
                pairs.append((syn, syntax[ref]))

        return pairs

    def get_and_conj_pair(self, text):
        syntax = self.get_syntax(text)

        pairs = []
        for syn in syntax:
            ref = int(syn[6]) - 1
            if syn[1] == 'и' and syn[7] == 'cc':
                first = syntax[ref]
                first_ref = int(first[6]) - 1
                if first[7] == 'conj':
                    pairs.append((first, syntax[first_ref]))

        return pairs
