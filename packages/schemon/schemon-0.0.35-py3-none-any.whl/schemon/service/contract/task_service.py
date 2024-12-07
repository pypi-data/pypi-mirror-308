from typing import List
from schemon.domain.contract import Task


def load_tasks(data: List[dict]) -> List[Task]:
    tasks = []
    for task_data in data:
        name = task_data.get("name")
        order = task_data.get("order")
        tasks.append(Task(name=name, order=order))
    return tasks
