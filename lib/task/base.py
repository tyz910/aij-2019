import re
import nltk
import unicodedata
from typing import Dict, List, Optional, Any


class Task:
    TYPE_UNKNOWN = 'unknown'
    TYPE_01 = '01'
    TYPE_02 = '02'
    TYPE_03 = '03'
    TYPE_04 = '04'
    TYPE_05 = '05'
    TYPE_06 = '06'
    TYPE_07 = '07'
    TYPE_08 = '08'
    TYPE_09 = '09'
    TYPE_10 = '10'
    TYPE_13 = '13'
    TYPE_14 = '14'
    TYPE_15 = '15'
    TYPE_16 = '16'
    TYPE_17 = '17'
    TYPE_21 = '21'
    TYPE_22 = '22'
    TYPE_23 = '23'
    TYPE_24 = '24'
    TYPE_25 = '25'
    TYPE_26 = '26'
    TYPE_27 = '27'

    def __init__(self, data: Dict):
        self.id: str = data['id']
        self.type: str = Task.TYPE_UNKNOWN
        self.text: str = data['text']
        self.question: Dict = data['question']
        self.score: float = float(data['score'])

        self.solution = None
        self.answer = None
        if 'solution' in data:
            self.solution = data['solution']

        self.data = data

    def __fix_numbered_lines_text(self, text: str) -> str:
        text = re.sub(r'([^,а-я]) ([0-9ЗО]{1,2}\))', r'\g<1>(\g<2>', self._to_line(text))
        return text

    def get_numbered_lines(self, text: Optional[str] = None, blacklist: List[str] = None) -> List[str]:
        if text is None:
            text = self.text

        text = self.__fix_numbered_lines_text(text)
        lines = re.split(r'\([0-9ЗО]{1,2}\)', text)
        lines = list(filter(None, map(str.strip, lines)))

        if blacklist is not None:
            for i, line in enumerate(lines):
                cut = False
                for stopword in blacklist:
                    if stopword.lower() in line.lower():
                        cut = True
                        break

                if not cut:
                    lines = lines[i:]
                    break

            while True:
                if len(lines) == 0:
                    break

                last = lines[-1]
                for stopword in blacklist:
                    parts = re.split(r'(' + re.escape(stopword) + ')(?i)', last)
                    if len(parts) > 1:
                        last = parts[0].strip()

                if last != '':
                    lines[-1] = last
                    break
                else:
                    lines = lines[:-1]

        return lines

    def remove_numbered_lines(self, lines: List[str], text: Optional[str] = None):
        if text is None:
            text = self.text
        text = self.__fix_numbered_lines_text(text)

        for line in lines:
            text = re.sub(r'\([0-9ЗО]{1,2}\) *' + re.escape(line), '', text)

        return self._to_line(text)

    def split_lines(self, text: Optional[str] = None) -> List[str]:
        if text is None:
            text = self.text
        text = re.sub(r'(\.|!|\?)([А-ЯЁ])', r'\g<1> \g<2>', text)  # Слипшиеся предложения

        lines = []
        for line in text.split('\n'):
            lines += nltk.sent_tokenize(line, language='russian')

        return list(map(str.strip, lines))

    def _to_line(self, text: str) -> str:
        text = text.replace('\n', ' ').replace('\t', ' ').strip()
        return ' '.join(text.split())

    def get_score(self, answer: Any) -> float:
        return 0.0

    def __repr__(self) -> str:
        return {
            'id': self.id,
            'type': self.type,
            'text': self.text,
            'question': self.question,
            'score': self.score,
        }.__repr__()


class TextTask(Task):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.answer: List[str] = []

        if self.solution is not None:
            if 'correct' in self.solution:
                self.answer = [self.solution['correct']]
            elif 'correct_variants' in self.solution:
                self.answer = self.solution['correct_variants']

    def get_score(self, answer: str) -> float:
        if answer in self.answer:
            return 1.0 * self.score

        return 0.0


class MultipleChoiceTask(Task):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.answer: List[str] = []
        self.choices: List[Dict] = self.question['choices']
        self.__fix_choices()

        if self.solution is not None:
            if 'correct' in self.solution:
                self.answer = self.solution['correct']
            elif 'correct_variants' in self.solution:
                self.answer = self.solution['correct_variants'][0]

    def __fix_choices(self):
        for i, choice in enumerate(self.question['choices']):
            if 'text' in choice:
                self.choices[i]['text'] = re.sub(r'^[0-9A-ZА-Я]+\)', '', choice['text']).strip()

    def get_score(self, answer: List[str]) -> float:
        y_true = set(self.answer)
        y_pred = set(answer)
        return 1.0 * self.score * int(len(set.intersection(y_true, y_pred)) == len(y_true) == len(y_pred))


class ChoiceTask(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.answer: str

        if self.solution is not None:
            if 'correct' in self.solution:
                self.answer = self.solution['correct'][0]

    def get_score(self, answer: str) -> float:
        # TODO Sber hack
        if isinstance(answer, list):
            return int(self.answer in answer) * self.score

        if answer == self.answer:
            return 1.0 * self.score

        return 0.0


class MatchingTask(MultipleChoiceTask):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.answer: Dict[str, str] = {}
        self.left: List[Dict] = self.question['left']
        self.__fix_left()

        if self.solution is not None:
            if 'correct' in self.solution:
                self.answer = {str(k): str(v) for k, v in self.solution['correct'].items()}

    def __fix_left(self):
        for i, left in enumerate(self.question['left']):
            if 'text' in left:
                self.left[i]['text'] = re.sub(r'^[0-9A-ZА-Я]+\)', '', left['text']).strip()

    def get_score(self, answer: Dict[str, str]) -> float:
        scores: List[float] = []

        for k, v in self.answer.items():
            if k in answer and answer[k] == v:
                scores.append(1.0)
            else:
                scores.append(0.0)

        return (sum(scores) / len(scores)) * self.score
