import os
import unittest
from app.constants import path, db_path
from app.database import initialize
from app.application import list_tasks, add_tasks


def create_db():
    os.makedirs(path, exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
    initialize()

def fill_db():
    add_tasks("Task 1", "Description 1", 1)


class Tasks(unittest.TestCase):
    def test_list_task(self):
        # set test environment
        create_db()
        # Test with no entries in table
        self.assertEqual(list_tasks(), [])


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
        "expected": []
        })

        for test in tests:
            self.assertEqual(list_tasks(**test["params"]), test["expected"])


if __name__ == '__main__':
    unittest.main()
