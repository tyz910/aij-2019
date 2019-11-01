import re
from lib.task.base import Task, TextTask
from typing import Dict, List, Optional


class Task02(TextTask):
    WORD_TYPES = {
        'союзное слово': 0,
        'подчинительный союз': 1,
        'сочинительный союз': 2,
        'местоимение': 3,
        'частицу': 4,
        'наречие': 5,
        'unknown': 6,
    }

    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_02

        self.candidates = []

        match = re.search(r'Какое из приведённых [^?]+\?([^(]+)\(', self.text)
        if match is not None:
            line = match.group(1).replace('Выпишите это слово', '').strip()
            line = re.sub(r'[^-А-Яа-яЁё ]', '', line)
            self.candidates = re.findall(r'[А-ЯЁ][-а-яё ]+', line)

        self.word_type: str = self.__get_word_type(self.text)
        self.missed_text: str = ''

        lines = self.get_numbered_lines()
        missed_idx = -1

        for i, line in enumerate(lines):
            if '<...>' in line:
                missed_idx = i
                lines[i] = line.replace('<...>', '[MASK]')
                break

            if '<…>' in line:
                missed_idx = i
                lines[i] = line.replace('<…>', '[MASK]')
                break

        if missed_idx == -1:
            for i, line in enumerate(lines):
                if '...' in line and not line.endswith('...'):
                    missed_idx = i
                    lines[i] = line.replace('...', '[MASK]')
                    break

                if '…' in line and not line.endswith('…'):
                    missed_idx = i
                    lines[i] = line.replace('…', '[MASK]')
                    break

        if missed_idx != -1:
            if missed_idx > 0:
                self.missed_text = ' '.join(['[CLS]', lines[missed_idx - 1], '[SEP]', lines[missed_idx], '[SEP]'])
            else:
                self.missed_text = ' '.join(['[CLS]', lines[missed_idx], '[SEP]'])

    @staticmethod
    def __get_word_type(text: str) -> str:
        if 'союзное слово' in text or 'относительное местоимение' in text:
            return 'союзное слово'

        if 'подчинительный' in text and 'союз' in text:
            return 'подчинительный союз'

        if 'сочинительный' in text and 'союз' in text:
            return 'сочинительный союз'

        if 'местоимение' in text:
            return 'местоимение'

        if 'частицу' in text:
            return 'частицу'

        if 'наречие' in text:
            return 'наречие'

        return 'unknown'
