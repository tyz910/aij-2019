import os
import pickle
import lightgbm as lgb
import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder as SklearnLabelEncoder
from catboost import CatBoostClassifier
from typing import List, Optional


class LgbClassifier:
    NUM_FOLDS = 5

    def __init__(self, model_name: str):
        self.model: Optional[lgb.Booster] = None
        self.model_name: str = model_name

        model_file = self.__get_model_path(model_name)
        if os.path.isfile(model_file):
            self.model = lgb.Booster(model_file=model_file)

    def train(self, X: np.array, y: np.array, num_folds: int = None, num_class: int = None) -> lgb.Booster:
        if num_class is None:
            num_class = 2

        params = {
            'task': 'train',
            'boosting_type': 'gbdt',
            'objective': 'multiclass',
            'num_class': num_class,
            'metric': 'multi_logloss',
            "learning_rate": 0.01,
            "num_leaves": 200,
            "feature_fraction": 0.70,
            "bagging_fraction": 0.70,
            'bagging_freq': 4,
            "max_depth": -1,
            "verbosity": -1,
            "reg_alpha": 0.3,
            "reg_lambda": 0.1,
            "min_child_weight": 10,
            'zero_as_missing': True,
            'num_threads': 4,
            'seed': 1,
        }

        if num_folds is None:
            num_folds = self.NUM_FOLDS

        iterations = []
        scores = []

        kf = KFold(n_splits=num_folds, random_state=1, shuffle=True)
        for train_index, test_index in kf.split(X):
            model = lgb.train(
                params,
                lgb.Dataset(X[train_index], label=y[train_index]),
                5000,
                lgb.Dataset(X[test_index], label=y[test_index]),
                early_stopping_rounds=15,
                verbose_eval=500
            )

            iterations.append(model.best_iteration)
            scores.append(model.best_score['valid_0']['multi_logloss'])

        best_iteration = int(np.mean(iterations))
        print(iterations)
        print(best_iteration)
        print()
        print(scores)
        print(np.mean(scores))

        self.model = lgb.train(
            params,
            lgb.Dataset(X, label=y),
            best_iteration,
        )

        return self.model

    def predict(self, X: np.array) -> np.array:
        return self.model.predict(X)

    def save(self, model_name: Optional[str] = None):
        if model_name is None:
            model_name = self.model_name

        self.model.save_model(self.__get_model_path(model_name))

    def __get_model_path(self, name: str) -> str:
        model_dir = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/lgb')
        return f'{model_dir}/{name}.txt'


class CtbClassifier:
    NUM_FOLDS = 5

    def __init__(self, model_name: str):
        self.model: Optional[CatBoostClassifier] = None
        self.model_name: str = model_name

        model_file = self.__get_model_path(model_name)
        if os.path.isfile(model_file):
            self.model = CatBoostClassifier().load_model(model_file)

    def train(self, X: np.array, y: np.array, num_folds: int = None, num_class=None) -> CatBoostClassifier:
        if num_folds is None:
            num_folds = self.NUM_FOLDS

        learning_rate = 0.1
        iterations = []
        scores = []

        if self.model_name == 'task08':
            learning_rate = 0.1
            best_iteration = 350
            #best_iteration = 256
        elif self.model_name == 'task17':
            learning_rate = 0.1
            best_iteration = 110
        elif self.model_name == 'task25--':
            learning_rate = 0.1
            best_iteration = 16
        else:
            kf = KFold(n_splits=num_folds, random_state=1, shuffle=True)
            for train_index, test_index in kf.split(X):
                model = CatBoostClassifier(iterations=5000, learning_rate=learning_rate, task_type="GPU")
                model.fit(
                    X[train_index], y[train_index], eval_set=(X[test_index], y[test_index]),
                    metric_period=15,
                    early_stopping_rounds=15,
                )

                iterations.append(model.best_iteration_)
                validation = model.best_score_['validation']
                scores.append(list(validation.values())[0])

            best_iteration = int(np.mean(iterations))
            print(iterations)
            print(best_iteration)
            print()
            print(scores)
            print(np.mean(scores))

        self.model = CatBoostClassifier(iterations=best_iteration, learning_rate=learning_rate, task_type="GPU")
        self.model.fit(X, y)

        return self.model

    def predict(self, X: np.array) -> np.array:
        return self.model.predict_proba(X)

    def save(self, model_name: Optional[str] = None):
        if model_name is None:
            model_name = self.model_name

        self.model.save_model(self.__get_model_path(model_name))

    def __get_model_path(self, name: str) -> str:
        model_dir = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/ctb')
        return f'{model_dir}/{name}.bin'


class LabelEncoder:
    def __init__(self, encoder_name: str):
        self.encoder: Optional[SklearnLabelEncoder] = None
        self.encoder_name: str = encoder_name

        model_file = self.__get_encoder_path(encoder_name)
        if os.path.isfile(model_file):
            with open(model_file, 'rb') as f:
                self.encoder = pickle.load(f)

    def fit(self, y: List[str]):
        self.encoder = SklearnLabelEncoder()
        self.encoder.fit(y + ['UNKNOWN'])

    def transform(self, y: str) -> int:
        if y not in self.encoder.classes_:
            y = 'UNKNOWN'

        return self.encoder.transform([y])[0]

    def get_num_class(self) -> int:
        return len(self.encoder.classes_)

    def __get_encoder_path(self, name: str) -> str:
        encoder_dir = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/encoder')
        return f'{encoder_dir}/{name}.pkl'
