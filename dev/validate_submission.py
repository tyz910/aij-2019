import sys
sys.path.append('.')

import json
from lib.ololosh import OloloshAI
from lib.task import create_tasks
from lib.sberbank.utils import rus_tok

ai = OloloshAI()
scores = []

for i in range(10):
    with open(f'var/data/check/test_0{i}.json') as fin:
        exam = json.load(fin)
        tasks = create_tasks(exam['tasks'])
        answers = ai.solve(tasks)

        score = 0
        max_score = 0
        for task in tasks:
            answer = answers[task.id]
            score += task.get_score(answer)
            max_score += task.score

        print(f'Score: {score} / {max_score}')
        scores.append(score)

total_score = sum(scores) / len(scores)
print(f'Total score: {total_score}')
