import sys
sys.path.append('..')

import json
from lib.ololosh import OloloshAI
from lib.task import create_tasks, Task1Task

ai = OloloshAI()
#exam_path = 'var/data/check/test_05.json'
#exam_path = 'var/data/yandex/04-stress.json'
exam_path = 'var/data/yandex/01-task.json'

with open(exam_path) as fin:
    exam = json.load(fin)

tasks = create_tasks(exam['tasks'])
answers = ai.solve(tasks)

score = 0
max_score = 0

for task in tasks:
    if not isinstance(task, Task1Task):
        print(task)
        print('FAIL!!!')
        exit(1)

    answer = answers[task.id]
    score += task.get_score(answer)
    max_score += task.score

    print('===========================')
    print(task.id)
    print(task.text[:100])
    print(task.answer)
    print(answer)
    print()

print(f'Score: {score} / {max_score}')
