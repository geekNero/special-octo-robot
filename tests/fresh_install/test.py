import subprocess
import unittest
from app.constants import path, db_path, config_path
from app.database import initialize
import os
import json

def create_db():
    os.makedirs(path, exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
    initialize("tasks")

class TestFreshInstall(unittest.TestCase):
    def test_list_task_with_empty_db(self):
        create_db()
        p = subprocess.run(("../verify_debug.sh"), shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        
        r = subprocess.run(("devcord tasks --list"), shell=True, capture_output=True, text=True)
        # verify output
        with open("test_list_task_with_empty_db") as exp:
            self.assertEqual(str(r.stdout).strip(), exp.read())
        # verify config file    
        with open(config_path) as act, open("test_list_task_with_empty_db_config.json") as exp:
            act_cfg = json.load(act)
            exp_cfg = json.load(exp)
            self.assertEqual(act_cfg,exp_cfg )
    
    def test_add_task_with_empty_db(self):
        create_db()
        p = subprocess.run(("../verify_debug.sh"), shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        
        r = subprocess.run(("devcord tasks --add 'test task'"), shell=True, capture_output=True, text=True)
        # verify output
        self.assertEqual(str(r.stdout).strip(), "")
