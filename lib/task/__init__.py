from lib.task.base import Task, TextTask, ChoiceTask, MultipleChoiceTask, MatchingTask
from lib.task.task01 import Task01
from lib.task.task02 import Task02
from lib.task.task03 import Task03
from lib.task.task04 import Task04
from lib.task.task05 import Task05
from lib.task.task06 import Task06
from lib.task.task07 import Task07
from lib.task.task08 import Task08
from lib.task.task09 import Task09
from lib.task.task10 import Task10, Task10Text, Task10MultipleChoice
from lib.task.task13 import Task13
from lib.task.task14 import Task14
from lib.task.task15 import Task15
from lib.task.task16 import Task16
from lib.task.task17 import Task17
from lib.task.task21 import Task21
from lib.task.task22 import Task22
from lib.task.task23 import Task23
from lib.task.task24 import Task24
from lib.task.task25 import Task25
from lib.task.task26 import Task26
from lib.task.task27 import Task27
from typing import Dict, List


def create_task(data: Dict) -> Task:
    task = Task(data)
    text = task.text.lower()
    text = ' '.join(text.split())

    if task.question['type'] == 'text':
        if 'напишите сочинение' in text:
            return Task27(data)

        if 'допущена ошибка в постановке ударения' in text:
            return Task04(data)

        if 'неверно употреблено' in text:
            return Task05(data)

        if 'исправьте лексическую ошибку' in text:
            return Task06(data)

        if 'ошибка в образовании формы слова' in text:
            return Task07(data)

        if 'пропущена одна и та же буква' in text or 'на месте пропуска пишется' in text:
            return Task10Text(data)

        if 'словом пишется слитно' in text:
            return Task13(data)

        if 'слова пишутся слитно' in text:
            return Task14(data)

        if 'выпишите' in text and 'из предложени' in text:
            return Task24(data)

        if 'самостоятельно подберите' in text or 'на месте пропуска' in text:
            return Task02(data)

        return TextTask(data)

    if task.question['type'] == 'choice':
        if 'значения слова' in text and 'предложении текста' in text:
            return Task03(data)

        return ChoiceTask(data)

    if task.question['type'] == 'multiple_choice':
        if 'в соответствии с одним и тем же правилом пунктуации' in text:
            return Task21(data)

        if 'соответствуют содержанию текста' in text or 'соответствует содержанию текста' in text:
            return Task22(data)

        if 'противоречат содержанию текста' in text:
            return Task22(data)

        if 'утверждений являются верными' in text or 'утверждений являются ошибочными' in text:
            return Task23(data)

        if 'реди предложений' in text and 'найдите' in text:
            return Task25(data)

        if 'пишется н.' in text or 'пишется нн.' in text or 'пишется одна буква н' in text:
            return Task15(data)

        if 'расставьте' in text and 'знаки препинания' in text:
            if 'укажите предложение' in text or 'укажите два предложения' in text or 'укажите номера предложений' in text:
                return Task16(data)

            if 'запятая' in text or 'запятые' in text:
                return Task17(data)

        if 'передана главная информация' in text:
            return Task01(data)

        if 'пропущена одна и та же буква' in text or 'на месте пропуска пишется' in text:
            return Task10MultipleChoice(data)

        if 'пропущена' in text and 'гласная корня' in text:
            return Task09(data)

        return MultipleChoiceTask(data)

    if task.question['type'] == 'matching':
        if 'соответствие между грамматическими ошибками' in text:
            return Task08(data)

        if 'соответствие между грамматической ошибкой' in text:
            return Task08(data)

        if 'допущенными в них грамматическими ошибками' in text:
            return Task08(data)

        if 'прочитайте фрагмент рецензии' in text:
            return Task26(data)

        return MatchingTask(data)

    return task


def create_tasks(data: List[Dict]) -> List[Task]:
    tasks = []

    for d in data:
        try:
            task = create_task(d)
        except Exception:
            task = Task(d)

        tasks.append(task)

    return tasks
