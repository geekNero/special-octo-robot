import sqlite3

from .constants import db_path


version_change_list = [
    ("0.0.8", """ALTER TABLE tasks ADD COLUMN subtask INTEGER DEFAULT 0;"""),
]


def run_migrations(previous_version):
    currect_version_index = -1
    for i in range(len(version_change_list)):
        if version_change_list[i][0] >= previous_version:
            currect_version_index = i
            break
    # if the version is equal start migrations from next version
    if previous_version == version_change_list[currect_version_index][0]:
        currect_version_index += 1

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # starts from the next version
    try:
        for i in range(currect_version_index, len(version_change_list)):
            cur.execute(version_change_list[i][1])
            conn.commit()
        conn.close()
        return 0
    except:
        conn.close()
        return 1
