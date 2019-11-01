import sys
sys.path.append('..')

from dev.loader import *
from lib.task import *
from lib.solver import *
from lib.sberbank.utils import rus_tok

solvers = [
    # (Task01, Task01Solver, ['01']),
    # (Task02, Task02Solver, ['02']),
    # (Task03, Task03Solver, ['03']),
    # (Task04, Task04Solver, ['04']),
    # (Task05, Task05Solver, ['05']),
    # (Task06, Task06Solver, ['06']),
    # (Task07, Task07Solver, ['07']),
    # (Task08, Task08Solver, ['08']),
    # (Task09, Task09Solver, ['09']),
    # (Task10, Task10Solver, ['10', '11', '12']),
    # (Task13, Task13Solver, ['13']),
    # (Task14, Task14Solver, ['14']),
    # (Task15, Task15Solver, ['15']),
    # (Task16, Task16Solver, ['16']),
    (Task17, Task17Solver, ['17', '18', '19', '20']),
    # (Task21, Task21Solver, ['21']),
    # (Task22, Task22Solver, ['22']),
    # (Task23, Task23Solver, ['23']),
    # (Task24, Task24Solver, ['24']),
    # (Task25, Task25Solver, ['25']),
    # (Task26, Task26Solver, ['26']),
]

for taskType, solverType, whitelist in solvers:
    print(taskType)
    # tasks = get_tasks_from_yandex(taskType, whitelist, ignore_ids=['35', '36'])
    tasks = get_tasks_from_yandex(taskType, whitelist)
    solver: BaseSolver = solverType()
    solver.train(tasks, save=True)

