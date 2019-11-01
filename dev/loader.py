import os
import json
from lib.task import create_tasks


def get_data_path(rel_path):
    return os.path.abspath(os.path.dirname(__file__) + '/../var/data') + rel_path


def get_tasks_from_check(taskType, whitelist):
    tasks = []

    for i in range(10):
        with open(get_data_path(f'/check/test_0{i}.json')) as fin:
            exam = json.load(fin)
            for t in create_tasks(exam['tasks']):
                task_id = t.id
                if len(task_id) == 1:
                    task_id = '0' + task_id

                if isinstance(t, taskType):
                    if task_id not in whitelist:
                        print('FAIL wrong task converted!!!')
                        print(type(t).__name__)
                        print(t)
                        exit()
                    tasks.append(t)
                elif task_id in whitelist:
                    print('FAIL task not converted !!!')
                    print(type(t).__name__)
                    print(t)
                    exit()

    for i, t in enumerate(tasks):
        t.id = t.data['id'] = str(i)

    return tasks


def get_tasks_from_yandex(taskType, whitelist, ignore_ids=None):
    tasks = []

    tid = 0
    for i in whitelist:
        with open(get_data_path(f'/yandex/task{i}.json')) as fin:
            exam = json.load(fin)
            for t in create_tasks(exam['tasks']):
                tid += 1
                t.id = t.data['id'] = str(tid)
                if ignore_ids is not None and t.id in ignore_ids:
                    continue

                if isinstance(t, taskType):
                    tasks.append(t)
                else:
                    print('FAIL!!!')
                    print(type(t).__name__)
                    print(t)
                    exit()

    return tasks
