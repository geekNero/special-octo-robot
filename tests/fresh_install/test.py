import subprocess
import unittest
from app.constants import path, db_path, config_path
from app.database import initialize
from app.database import insert_into_table
import os
import json

def create_db_and_config():
    os.makedirs(path, exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
        os.remove(config_path)
    initialize("tasks")

class TestFreshInstall(unittest.TestCase):
    def test_list_task_with_empty_db(self):
        create_db_and_config()
        p = subprocess.run(("../verify_debug.sh"), shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        
        r = subprocess.run(("devcord tasks --list"), shell=True, capture_output=True, text=True)
        # verify output

        self.assertEqual(str(r.stdout).strip(), "Info: No tasks found.")
        # verify config file    
        with open(config_path) as act, open("test_list_task_with_empty_db_config.json") as exp:
            act_cfg = json.load(act)
            exp_cfg = json.load(exp)
            self.assertEqual(act_cfg,exp_cfg )
    
    def test_add_task_with_empty_db(self):
        create_db_and_config()
        p = subprocess.run(("../verify_debug.sh"), shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        
        r = subprocess.run(("devcord tasks --add 'test task'"), shell=True, capture_output=True, text=True)
        # verify output
        self.assertEqual(str(r.stdout).strip(), "")

        r = subprocess.run(("devcord tasks --list"), shell=True, capture_output=True, text=True)
        with open("test_add_task_with_empty_db") as exp:
            self.assertEqual(str(r.stdout), exp.read())
    
    def test_table_operations_with_empty_db(self):
        create_db_and_config()
        p = subprocess.run(("../verify_debug.sh"), shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        
        r = subprocess.run(("devcord tables -a 'test table'"), shell=True, capture_output=True, text=True)
        # verify output
        self.assertEqual(str(r.stdout).strip(), "Success: Table stored as test_table")

        r = subprocess.run(("devcord tables -l"), shell=True, capture_output=True, text=True)

        with open("test_list_table_with_empty_db") as exp:
            self.assertEqual(str(r.stdout), exp.read())
        
        r = subprocess.run(("devcord tables -dl 'testtable'"), shell=True, capture_output=True, text=True)
        
        self.assertEqual(str(r.stdout).strip(), "Error: Table does not exist.")
        
        r = subprocess.run(("devcord tables -sl 'test_table'"), shell=True, capture_output=True, text=True)
        
        self.assertEqual(str(r.stdout).strip(), "Success: Table selected test_table")
        
        with open("test_select_table_with_empty_db_config.json") as exp, open(config_path) as act:
            self.assertEqual(json.load(act), json.load(exp))
        
    def test_init_with_empty_db(self):
        create_db_and_config()
        p = subprocess.run(("../verify_debug.sh"), shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        
        r = subprocess.run(("devcord init --pretty_tree False"), shell=True, capture_output=True, text=True)
        # verify output
        self.assertEqual(str(r.stdout).strip(), "Info: Pretty Tree setting updated")
        
        with open("test_init_with_empty_db_config.json") as exp, open(config_path) as act:
            self.assertEqual(json.load(act), json.load(exp))
            
        insert_into_table("tasks", ["title" ], ["'parent'"])
        insert_into_table("tasks", ["title", "parent_id" ], ["'child'", "1"])
        
        r = subprocess.run(("devcord tasks --list -st"), shell=True, capture_output=True, text=True)
        with open("test_list_task_with_empty_db_subtasks") as exp:
            self.assertEqual(str(r.stdout), exp.read())
        