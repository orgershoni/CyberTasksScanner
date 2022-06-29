from datetime import datetime
from uuid import uuid4
from enum import Enum
from typing import List, Dict, Any


class TaskStatus(Enum):
    Accepted = 202
    Running = 201
    Error = 400
    Complete = 200
    NotFound = 404


class CyberScanTask:
    def __init__(self):
        self.created_at = datetime.now()
        self.fetched = False
        self.id = str(uuid4())
        self.raise_error = False

    def to_dict(self):
        return {
            "created_at": str(self.created_at),
            "fetched": self.fetched,
            "id": self.id,
            "raise_error": self.raise_error
        }

    @staticmethod
    def from_dict(dict_var):
        task = CyberScanTask()
        task.created_at = dict_var['created_at']
        task.id = dict_var['id']
        task.fetched = dict_var['fetched']
        task.raise_error = dict_var['raise_error']
        return task


class CyberScanTable:
    def __init__(self):
        self.table: Dict[str, CyberScanTask] = dict()

    def create(self, params) -> Dict[str, Any]:
        scan = CyberScanTask()
        as_dict = scan.to_dict()
        as_dict = CyberScanTable._update_task_fields(as_dict, params)
        self.table[scan.id] = CyberScanTask.from_dict(as_dict)
        return as_dict

    @staticmethod
    def _update_task_fields(task, updated_fields):
        for (field, value) in updated_fields.items():
            if field in task.keys():
                task[field] = value
        return task

    def update(self, task_id, updated_fields: Dict[str, Any]) -> Dict[str,
                                                                      Any]:
        if task_id not in self.table.keys():
            return None
        scan = self.table[task_id].to_dict()
        scan = CyberScanTable._update_task_fields(scan, updated_fields)
        self.table[task_id] = CyberScanTask.from_dict(scan)
        return scan

    def find_by_id(self, task_id: str) -> Dict[str, Any]:
        task = self.table.get(task_id)
        if not task:
            return None
        return task.to_dict()

    def fetch_pending_tasks(self, num_tasks) -> List[Dict[str, Any]]:
        legal_tasks = list(filter(lambda task: not task.fetched,
                                  self.table.values()))
        pending_tasks = [task.to_dict() for task in
                         sorted(legal_tasks,
                         key=lambda task: task.created_at)]
        return pending_tasks[:num_tasks]


class MongoDB:

    def __init__(self):
        self.table: Dict[str, int] = dict()

    def init_entry(self, task_id):
        if task_id not in self.table.keys():
            self.table[task_id] = TaskStatus.Accepted.value
        return self.table.get(task_id)

    def set_status(self, task_id, status):
        if task_id in self.table.keys():
            self.table[task_id] = status
        return self.table.get(task_id)

    def get_status(self, task_id):
        return self.table.get(task_id, TaskStatus.NotFound.value)


# initialize Mock DBs
tasks_table = CyberScanTable()
mongo_status_table = MongoDB()