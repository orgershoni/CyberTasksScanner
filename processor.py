from db_wrapper import TaskStatus
import time
from configs.config import app_url
import sys
import requests
from typing import List, Dict, Any
from configs.config import global_config as config

EXECUTION_DURATION_SECS = 10


def process_task(task: Dict[str, Any]):
    task['status'] = TaskStatus.Running.value
    update_url = f'{app_url}/api/update_task/{task["id"]}'
    r = requests.patch(update_url, json=task)
    if r.status_code != 200:
        print(f'Failed to update task {task["id"]}. Reason: {r.json()}')
    try:
        # Mocking execution of task
        time.sleep(EXECUTION_DURATION_SECS)
        task['status'] = TaskStatus.Complete.value
        if task['raise_error']:
            raise Exception(f'Indented error occurred while processing task '
                            f'{task["id"]}')
    except Exception:
        task['status'] = TaskStatus.Error.value
    finally:
        r = requests.patch(update_url, json=task)
        if r.status_code != 200:
            print(f'Failed to update task {task["id"]}. Reason: {r.json()}')


def bulk_process(tasks: List[Dict[str, Any]]):
    for task in tasks:
        process_task(task)


def listen_for_tasks():
    try:
        params = {'num_tasks': config.get('max_tasks_to_process', 1)}
        r = requests.get(f'{app_url}/api/fetch_tasks/', params=params)
        if r.status_code != 200:
            print(f'Failed to fetch tasks. Reason {r.json()}')
            return
        tasks = r.json()
        print(f'Tasks are {tasks}')
        bulk_process(tasks)
    except Exception as e:
        print(f'Error occurred while processing tasks: {e}', file=sys.stderr)
    finally:
        time.sleep(10)


def work():
    try:
        while True:
            listen_for_tasks()
    except KeyboardInterrupt:
        exit(0) # Exit quietly


if __name__ == '__main__':
    work()


# TODO:
#  (2) Add postman schema
#  (3) Save statuses in dynamoDB
#  (4) Add README