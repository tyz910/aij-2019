import sys
sys.path.append('..')

from dev.loader import *
from lib.task import *
from lib.solver import *
from lib.sberbank.utils import rus_tok

tasks = get_tasks_from_yandex(Task10, ['10', '11', '12'])

solver = Task10Solver()
# solver = SberbankSolver(solver_ids=[15])

score = 0
max_score = 0
for task in tasks:
    answer = solver.solve(task)
    answer_score = task.get_score(answer)
    score += answer_score
    max_score += task.score

    print('===========================')
    print(task.id)
    print(task.text[:100])
    print('correct', task.answer)
    print('answer', answer)
    print()

print(f'Score: {score} / {max_score}')
