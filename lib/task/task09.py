import re
from lib.task.base import Task, MultipleChoiceTask
from typing import Dict, List


class Task09(MultipleChoiceTask):
    RULE_PG = 'ПГ'
    RULE_NG = 'НГ'
    RULE_CG = 'ЧГ'

    def __init__(self, data: Dict):
        super().__init__(data)
        self.type = Task.TYPE_09

        self.lines = [re.findall(r'([а-яё]+\.\.[а-яё]+)', c['text'].lower()) for c in self.question['choices']]

        self.rule = None
        if 'непроверяемая' in self.text.lower():
            self.rule = self.RULE_NG
        elif 'проверяемая' in self.text.lower():
            self.rule = self.RULE_PG
        elif 'чередующаяся' in self.text.lower():
            self.rule = self.RULE_CG
