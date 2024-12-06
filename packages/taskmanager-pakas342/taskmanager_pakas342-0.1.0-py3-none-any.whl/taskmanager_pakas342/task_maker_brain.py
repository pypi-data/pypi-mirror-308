import json
import time
from datetime import datetime
from uuid import uuid4
from pathlib import Path


def find_index(seq: list[dict], key: str, value):
    for i, dictionary in enumerate(seq):
        if dictionary[key] == value:
            return i
    raise ValueError(f'element with {key} "{value}" not found')


def print_task(task):
    return print(f'Task id: {task['id']} - '
                 f'Task: {task['title']} - '
                 f'created: {datetime.fromtimestamp(task['created_at'])} - '
                 f'status: {"completed" if task['completed'] else "uncompleted"}')


class Task:
    """dataclass for a task"""

    def __init__(self, title: str):
        self.title: str = title
        self.created_at: int = int(time.time())
        self.completed: bool = False
        self.id: str = str(uuid4())


class TaskManager:
    def __init__(self):
        self.file = Path.cwd() / '.tasks.json'

    def get_tasks(self, completed: bool = False):
        file = self.file
        try:
            with open(file, 'r') as f:
                try:
                    task_types = json.load(f)
                    tasks = task_types['uncompleted_tasks'] if not completed else task_types['completed_tasks']
                except json.JSONDecodeError:
                    tasks = []
        except FileNotFoundError:
            tasks = []
        return tasks

    def update_tasks(self, uncompleted_tasks: json = None, completed_tasks: json = None):
        file = self.file
        if uncompleted_tasks is None:
            uncompleted_tasks = self.get_tasks()
        if completed_tasks is None:
            completed_tasks = self.get_tasks(completed=True)
        task_types = {
            'uncompleted_tasks': uncompleted_tasks,
            'completed_tasks': completed_tasks
        }
        with open(file, 'w') as f:

            json.dump(task_types, f)

    def add(self, task_title):
        if not task_title:
            raise TypeError('None task title given')
        tasks = self.get_tasks()

        # Done with a set {} instead of a list to achieve O(1)
        title_list = {task['title'] for task in tasks} if tasks else {}
        if task_title in title_list:
            raise Exception('Already Existing Task')

        new_task = Task(task_title)
        tasks.append(new_task.__dict__)

        self.update_tasks(uncompleted_tasks=tasks)

    def delete(self, task_id: str = None, task_title: str = None):
        if not task_id and not task_title:
            raise TypeError('None task id or task title given')
        tasks = self.get_tasks()

        if task_id:
            index = find_index(tasks, 'id', task_id)
        elif task_title:
            index = find_index(tasks, 'title', task_title)
        else:
            index = None

        tasks.pop(index)
        self.update_tasks(completed_tasks=tasks)

    def complete(self, task_id: str = None, task_title: str = None):
        if not task_id and not task_title:
            raise TypeError('None task id or task title given')
        uncompleted_tasks = self.get_tasks()

        if task_id:
            index = find_index(uncompleted_tasks, 'id', task_id)
        elif task_title:
            index = find_index(uncompleted_tasks, 'title', task_title)
        else:
            index = None

        uncompleted_tasks[index]['completed'] = True
        completed_task = uncompleted_tasks.pop(index)

        try:
            completed_tasks = self.get_tasks(completed=True)
        except (FileNotFoundError, json.JSONDecodeError):
            completed_tasks = []
        completed_tasks.append(completed_task)

        self.update_tasks(uncompleted_tasks=uncompleted_tasks, completed_tasks=completed_tasks)

    def read(self, task_id: str = None, task_title: str = None, read_all: bool = False, completed: bool = False):
        if not task_id and not task_title and not read_all:
            raise TypeError('None task id, task title, or read all given')
        tasks = self.get_tasks(completed=completed)
        if task_id:
            index = find_index(tasks, 'id', task_id)
            print_task(tasks[index])
        elif task_title:
            index = find_index(tasks, 'title', task_title)
            print_task(tasks[index])
        else:
            return [print_task(task) for task in tasks]


if __name__ == '__main__':
    testing_task_manager = TaskManager()
    testing_task_manager.read(task_title='test task 2', completed=True)
    testing_task_manager.read(read_all=True)
