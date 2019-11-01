from lib.task import Task
from lib.solver.base import BaseSolver
from typing import List, Dict, Any


class DummySolver(BaseSolver):
    def get_task_type(self) -> str:
        return Task.TYPE_UNKNOWN

    def solve(self, task: Task) -> Any:
        question = task.data['question']

        if question['type'] == 'choice':
            answer = question['choices'][0]['id']

        elif question['type'] == 'multiple_choice':
            answer = [choice['id'] for choice in question['choices']][:3]

        elif question['type'] == 'matching':
            answer = {left['id']: choice['id'] for left, choice in zip(question['left'], question['choices'])}

        elif question['type'] == 'text':
            if question.get('restriction') == 'word':
                words = [word for word in task.data['text'].split() if len(word) > 1]
                answer = words[0]

            else:
                # random text generated with https://fish-text.ru
                answer = (
                    'Для современного мира реализация намеченных плановых заданий позволяет '
                    'выполнить важные задания по разработке новых принципов формирования '
                    'материально-технической и кадровой базы. Господа, реализация намеченных '
                    'плановых заданий играет определяющее значение для модели развития. '
                    'Сложно сказать, почему сделанные на базе интернет-аналитики выводы призывают '
                    'нас к новым свершениям, которые, в свою очередь, должны быть в равной степени '
                    'предоставлены сами себе. Ясность нашей позиции очевидна: базовый вектор '
                    'развития однозначно фиксирует необходимость существующих финансовых и '
                    'административных условий.'
                )

        else:
            raise RuntimeError('Unknown question type: {}'.format(question['type']))

        return answer
