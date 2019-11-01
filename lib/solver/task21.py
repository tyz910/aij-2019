import re
from lib.task import Task, Task21
from lib.solver.base import BaseSolver
from lib.solver.sberbank import SberbankSolver
from lib.util.syntax import SyntaxParser
from typing import List, Dict, Any, Optional


class Task21Solver(BaseSolver):
    def __init__(self, syntax: Optional[SyntaxParser] = None, sberbank_solver: Optional[SberbankSolver] = None):
        if syntax is None:
            syntax = SyntaxParser()
        self.syntax: SyntaxParser = syntax

        if sberbank_solver is None:
            sberbank_solver = SberbankSolver()
        self.sberbank_solver: SberbankSolver = sberbank_solver

    def get_task_type(self) -> str:
        return Task.TYPE_21

    def solve(self, task: Task21) -> Any:
        lines = task.lines

        if task.question_type == '–':
            lines = self.dash_not_in_line(lines)

            filters = [
                (self.dash_has_number_range, 1),
                (self.dash_has_nsubj_over, 1),
                (self.dash_has_talk, 1),
                (self.dash_is_insert, 2),
                (self.dash_and, 1),
            ]

            for f, check_chars in filters:
                lines, group = self.filter_group('–', lines, f, check_chars)
                if group:
                    return self.to_answer(task, group)

        if len(lines) > 1:
            filtered_data = task.data.copy()
            filtered_data['text'] = task.question_text + ' ' + ' '.join([f'({i}) {line}' for i, line in enumerate(lines, 1)])
            filtered_data['question']['choices'] = [{
                "id": str(i),
                "link": f"({i})"
            } for i, line in enumerate(lines, 1)]


            sberbank_answer = self.sberbank_solver.solve(Task(filtered_data))
            sberbank_lines = [lines[int(i) - 1] for i in sberbank_answer]

            return self.to_answer(task, sberbank_lines)
        else:
            return self.sberbank_solver.solve(task)

    def to_answer(self, task, lines):
        return [str(i + 1) for i, line in enumerate(task.lines) if line in lines]

    def filter_group(self, char, lines, func, check_chars=1):
        in_group = []
        not_in_group = []

        for line in lines:
            if func(line):
                in_group.append(line)
            else:
                not_in_group.append(line)

        if len(in_group) > 1:
            return lines, in_group

        for line in in_group:
            if len(re.findall(re.escape(char), line)) > check_chars:
                not_in_group.append(line)

        return not_in_group, []

    def dash_not_in_line(self, lines):
        return [line for line in lines if '–' in line]

    # Тире для обозначения количественных пределов.
    def dash_has_number_range(self, line):
        return bool(re.search(r'[0-9]+\s*–\s*[0-9]+', line))

    def dash_has_nsubj_over(self, line):
        syntax = self.syntax.get_syntax(line)
        for node in syntax.nodes:
            if node.word == '–':
                first = node.get_link(ignore_types=['nmod'])

                if first and first.link_type == 'nsubj':
                    second = first.get_link()
                    if second.POS == 'VERB':
                        continue

                    return (first.id < node.id) and (second.id > node.id)

        return False

    def dash_has_talk(self, line):
        return bool(re.search(r'«[А-ЯЁ][^!?.»]+(!»|\?»|\.»|»,)\s–\s', line))

    def dash_is_insert(self, line):
        line = re.sub(r'«[^»]+»', '', line)
        return bool(re.search(r'[^–]{5,}– [-а-яё ]+[,!? ]*–[^–]+', line))

    def dash_and(self, line):
        return '– и ' in line
