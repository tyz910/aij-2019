from lib.task.base import Task, MatchingTask
from typing import Dict, List


class Task08(MatchingTask):
    CLASSES = {
        'error_connection подлежащим и сказуемым': 0,
        'error_form сущ': 1,
        'error_other': 2,
        'error_struct деепричастным оборотом': 3,
        'error_struct косвенной речью': 4,
        'error_struct несогласованным приложением': 5,
        'error_struct однородными членами': 6,
        'error_struct причастным оборотом': 7,
        'error_struct сложного предложения': 8,
        'error_time глагольных форм': 9,
        # 'correct': 10,
    }

    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_08

        self.left_labels: Dict[str, int] = {l['id']: self.get_left_class(l['text']) for l in self.left}

    def get_left_class(self, text: str) -> int:
        error_types = {
            'нарушение в построении предложения с': 'error_struct',
            'нарушение в построении': 'error_struct',
            'неправильное построение предложения с': 'error_struct',
            'ошибка в построении предложения с': 'error_struct',
            'нарушение в предложении с': 'error_struct',
            'неправильное построение': 'error_struct',
            'ошибка в построении': 'error_struct',
            'нарушение построения предложения с': 'error_struct',

            'неверный выбор падежной формы': 'error_form',
            'неверный выбор предложно-падежной формы': 'error_form',
            'неправильное употребление падежной формы': 'error_form',
            'неправильный выбор падежной формы': 'error_form',
            'неправильный выбор предложно-падежной формы': 'error_form',

            'нарушение видо-временной соотнесённости': 'error_time',
            'нарушение видовременной соотнесённости': 'error_time',
            'нарушение временной соотнесённости': 'error_time',

            'нарушение связи между': 'error_connection',
        }

        error_replaces = {
            'error_form': {
                'имени существительного': 'сущ',
                'имени существительного с предлогом': 'сущ',
                'существительного': 'сущ',
                'существительного с предлогом': 'сущ',
                'сущ с предлогом': 'сущ',
            },

            'error_struct': {
                'однородными членами предложения': 'однородными членами',
                'сложноподчинённого предложения': 'сложного предложения',
            }
        }

        text = text.lower().strip('. ')

        for e, r in error_types.items():
            text = text.replace(e, r)

        for error_type, replaces in error_replaces.items():
            for replace_from, replace_to in replaces.items():
                text = text.replace(replace_from, replace_to)

        if 'error' not in text or text not in self.CLASSES:
            text = 'error_other'

        return self.CLASSES[text]
