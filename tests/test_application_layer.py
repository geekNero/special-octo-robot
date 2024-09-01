import os
import unittest
from app.constants import path, db_path
from app.database import initialize
from app.application import list_tasks, add_tasks
from datetime import datetime, timedelta

def create_db():
    os.makedirs(path, exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
    initialize()

def fill_db():
    add_tasks(title = "Task 1", description="Description 1", priority=1)
    add_tasks(title = "Task 2", description="Description 2", priority=4, today=True)
    add_tasks(title = "Task 3", description="Description 3", priority=2, week=True)
    future_date = datetime.now() + timedelta(days=10)
    add_tasks(title = "Task 4", description="Description 4", priority=3, deadline=future_date.strftime("%Y-%m-%d"))
    add_tasks(title = "Task 5", description="Description 5", priority=5, completed=True)
    add_tasks(title = "Task 6", description="Description 6", inprogress=True)
    add_tasks(title = "Task 7", description="Description 7", pending=True)
    add_tasks(title = "Task 8", priority=3, deadline='2000-09-11')
    add_tasks(title='Child of task 1', parent={"id":1}, label='Label1')
    add_tasks(title='Child of child task 1', parent={"id": 9}, week=True)


class Tasks(unittest.TestCase):
    def test_list_task(self):
        # set test environment
        create_db()
        # Test with no entries in table
        self.assertEqual(list_tasks(), [])
        fill_db()

        tests = []
        # test case 1
        tests.append({
         "params": {
                "priority": None,
                "today": False,
                "week": False,
                "inprogress": False,
                "completed": False,
                "pending": False,
                "label": None,
                "subtasks": False,
            },
        "expected": [
    {
        "id": 8,
        "title": "Task 8",
        "parent_id": None,
        "status": "Pending",
        "deadline": "11/09/2000",
        "priority": 3,
        "label": "None",
        "description": "None",
        "subtasks": 0,
    },
    {
        "id": 2,
        "title": "Task 2",
        "parent_id": None,
        "status": "Pending",
        "deadline": "01/09/2024",
        "priority": 4,
        "label": "None",
        "description": "Description 2",
        "subtasks": 0,
    },
    {
        "id": 3,
        "title": "Task 3",
        "parent_id": None,
        "status": "Pending",
        "deadline": "01/09/2024",
        "priority": 2,
        "label": "None",
        "description": "Description 3",
        "subtasks": 0,
    },
    {
        "id": 4,
        "title": "Task 4",
        "parent_id": None,
        "status": "Pending",
        "deadline": "11/09/2024",
        "priority": 3,
        "label": "None",
        "description": "Description 4",
        "subtasks": 0,
    },
    {
        "id": 6,
        "title": "Task 6",
        "parent_id": None,
        "status": "In Progress",
        "deadline": "None",
        "priority": 0,
        "label": "None",
        "description": "Description 6",
        "subtasks": 0,
    },
    {
        "id": 1,
        "title": "Task 1",
        "parent_id": None,
        "status": "Pending",
        "deadline": "None",
        "priority": 1,
        "label": "None",
        "description": "Description 1",
        "subtasks": 1,
    },
    {
        "id": 7,
        "title": "Task 7",
        "parent_id": None,
        "status": "Pending",
        "deadline": "None",
        "priority": 0,
        "label": "None",
        "description": "Description 7",
        "subtasks": 0,
    },
]


        })

        for test in tests:
            self.assertEqual(list_tasks(**test["params"]), test["expected"])


if __name__ == '__main__':
    unittest.main()
