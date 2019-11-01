import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    from lib.solver.base import BaseSolver
    from lib.solver.dummy import DummySolver
    from lib.solver.zero import ZeroSolver, ZeroSberbankSolver
    from lib.solver.sberbank import SberbankSolver
    from lib.solver.task01 import Task01Solver
    from lib.solver.task02 import Task02Solver
    from lib.solver.task03 import Task03Solver
    from lib.solver.task04 import Task04Solver
    from lib.solver.task05 import Task05Solver
    from lib.solver.task06 import Task06Solver
    from lib.solver.task07 import Task07Solver
    from lib.solver.task08 import Task08Solver
    from lib.solver.task09 import Task09Solver
    from lib.solver.task10 import Task10Solver
    from lib.solver.task13 import Task13Solver
    from lib.solver.task14 import Task14Solver
    from lib.solver.task15 import Task15Solver
    from lib.solver.task16 import Task16Solver
    from lib.solver.task17 import Task17Solver
    from lib.solver.task21 import Task21Solver
    from lib.solver.task22 import Task22Solver
    from lib.solver.task23 import Task23Solver
    from lib.solver.task24 import Task24Solver
    from lib.solver.task25 import Task25Solver
    from lib.solver.task26 import Task26Solver
    from lib.solver.task27 import Task27Solver
