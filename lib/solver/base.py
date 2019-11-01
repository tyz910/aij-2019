import os
import pickle
import numpy as np
from lib.task.base import Task
from typing import List, Tuple, Any
from sklearn.model_selection import train_test_split, KFold


class BaseSolver:
    def get_task_type(self) -> str:
        raise NotImplementedError("Task type not specified")

    def solve(self, task: Task) -> Any:
        raise NotImplementedError("Solve method not implemented")

    def train(self, tasks: List[Task], save: bool = True):
        pass

    def validate(self, tasks: List[Task]) -> Tuple[float, float]:
        score = 0.0
        max_score = 0.0

        for task in tasks:
            answer = self.solve(task)
            score += task.get_score(answer)
            max_score += task.score

        return score, max_score

    def cross_validate(self, tasks: List[Task], n_splits=3) -> Tuple[float, float]:
        tasks = np.array(tasks)
        total_score = 0
        total_max_score = 0

        kf = KFold(n_splits=n_splits, random_state=42, shuffle=True)
        for train_idx, test_idx in kf.split(tasks):
            self.train(list(tasks[train_idx]), save=False)
            score, max_score = self.validate(list(tasks[test_idx]))
            total_score += score
            total_max_score += max_score

        return total_score, total_max_score

    def train_and_validate(self, tasks: List[Task]) -> Tuple[float, float]:
        tasks_train, tasks_test = train_test_split(tasks, test_size=0.1, random_state=42)
        self.train(tasks_train, save=False)
        return self.validate(tasks_test)

    def save_pkl(self, name: str, model):
        model_file = self.__get_pkl_path(name)
        with open(model_file, 'wb') as f:
            pickle.dump(model, f)

    def load_pkl(self, name: str):
        model_file = self.__get_pkl_path(name)
        if os.path.isfile(model_file):
            with open(model_file, 'rb') as f:
                return pickle.load(f)

        return None

    def __get_pkl_path(self, name: str) -> str:
        pkl_dir = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/pkl')
        return f'{pkl_dir}/{name}.pkl'
