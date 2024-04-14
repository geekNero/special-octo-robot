import sqlite3

from .constants import db_path


migration_list = [
    ("0.0.8", """ALTER TABLE tasks ADD COLUMN subtasks INTEGER DEFAULT 0;"""),
]


def run_migrations(previous_version):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for migration in migration_list:
        if migration[0] > previous_version:
            cur.execute(migration[1])
            conn.commit()
    conn.close()
