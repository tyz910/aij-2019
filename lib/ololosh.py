from lib.task import *
from lib.solver import *
from lib.util.bert import Bert
from lib.util.speller import Speller
from lib.util.stress import Stress
from lib.util.sentence_encoder import SentenceEncoder
from lib.util.esse import EsseLoader
from lib.util.ner import NER
from lib.util.syntax import SyntaxParser

from typing import Dict, List, Any, Optional


class OloloshAI:
    def __init__(
        self,
        solvers: List[BaseSolver] = None,
        bert: Optional[Bert] = None,
        speller: Optional[Speller] = None,
        stress: Optional[Stress] = None,
        sentence_encoder: Optional[SentenceEncoder] = None,
        esse: Optional[EsseLoader] = None,
        ner: Optional[NER] = None,
        syntax: Optional[SyntaxParser] = None,
        sberbank_solver: Optional[SberbankSolver] = None,
    ):
        self.bert: Bert = bert
        self.speller: Speller = speller
        self.stress: Stress = stress
        self.sentence_encoder: SentenceEncoder = sentence_encoder
        self.esse: EsseLoader = esse
        self.ner: NER = ner
        self.syntax: SyntaxParser = syntax
        self.sberbank_solver: SberbankSolver = sberbank_solver
        self.solvers: Dict[str, BaseSolver] = {}

        if solvers is None:
            self.__add_default_solvers()
        else:
            for solver in solvers:
                if self.sberbank_solver is None and isinstance(solver, SberbankSolver):
                    self.sberbank_solver = solver

                self.add_solver(solver)

    def __add_default_solvers(self):
        if self.bert is None:
            self.bert = Bert()

        if self.speller is None:
            self.speller = Speller()

        if self.stress is None:
            self.stress = Stress()

        if self.sentence_encoder is None:
            self.sentence_encoder = SentenceEncoder()

        if self.esse is None:
            self.esse = EsseLoader(sentence_encoder=self.sentence_encoder)

        if self.ner is None:
            self.ner = NER()

        if self.syntax is None:
            self.syntax = SyntaxParser(self.speller)

        if self.sberbank_solver is None:
            self.sberbank_solver = SberbankSolver()

        # self.add_solver(ZeroSolver())
        # self.add_solver(DummySolver())
        # self.add_solver(ZeroSberbankSolver(task_types=[
        #     Task24,
        # ]))

        self.add_solver(self.sberbank_solver)
        self.add_solver(Task01Solver(self.bert, self.sentence_encoder))
        self.add_solver(Task02Solver(self.bert, self.speller))
        self.add_solver(Task03Solver(self.bert, self.sentence_encoder))
        self.add_solver(Task04Solver(self.stress))
        self.add_solver(Task05Solver(self.bert, self.speller))
        self.add_solver(Task06Solver(self.bert, self.speller, self.sberbank_solver))
        self.add_solver(Task07Solver(self.speller))
        self.add_solver(Task08Solver(self.bert, self.speller, self.syntax))
        self.add_solver(Task09Solver(self.speller, self.stress))
        self.add_solver(Task10Solver(self.speller))
        self.add_solver(Task13Solver(self.bert, self.speller))
        self.add_solver(Task14Solver(self.bert, self.speller))
        self.add_solver(Task15Solver(self.bert, self.speller))
        self.add_solver(Task16Solver(self.bert))
        self.add_solver(Task17Solver(self.bert))
        self.add_solver(Task21Solver(self.syntax, self.sberbank_solver))
        self.add_solver(Task25Solver(self.bert, self.speller))
        self.add_solver(Task27Solver(self.esse, self.ner, self.sberbank_solver, self.syntax))

    def add_solver(self, solver: BaseSolver):
        self.solvers[solver.get_task_type()] = solver

    def take_exam(self, exam) -> Dict[str, Any]:
        tasks = create_tasks(exam)
        return self.solve(tasks)

    def solve(self, tasks: List[Task]) -> Dict[str, Any]:
        answers = {}

        for task in tasks:
            if task.type in self.solvers:
                solver = self.solvers[task.type]
            else:
                solver = self.solvers[Task.TYPE_UNKNOWN]

            try:
                answers[task.id] = solver.solve(task)
            except Exception:
                answers[task.id] = self.sberbank_solver.solve(task)

        return answers
