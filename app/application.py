import datetime
import json
import sqlite3
import time
from collections import defaultdict

from . import database
from app.constants import DEFAULT_TABLE
from app.constants import STATUS_COMPLETED
from app.constants import STATUS_IN_PROGRESS
from app.constants import STATUS_PENDING
from app.sessions.linux import session_end as linux_session_end
from app.sessions.linux import session_start as linux_session_start
from app.utility import convert_epoch_to_date
from app.utility import convert_epoch_to_datetime
from app.utility import convert_seconds_delta_to_time
from app.utility import convert_time_to_epoch
from app.utility import display_error_message
from app.utility import display_info_message
from app.utility import generate_migration_error
from app.utility import get_os
from app.utility import get_week_start
from app.utility import get_weekend
from app.utility import sanitize_text


def list_tasks(
    table=DEFAULT_TABLE,
    priority=None,
    today=None,
    week=None,
    date=None,
    inprogress=None,
    completed=None,
    pending=None,
    label=None,
    subtasks=False,
) -> list:
    """
    List all the tasks based on the filters.
    """
    order_by = "completed ASC, status ASC, priority DESC"
    where_clause = []
    params = []

    if not subtasks:
        where_clause.append("parent_id ISNULL")

    if week:
        mond = convert_time_to_epoch(get_week_start(), False)
        sund = convert_time_to_epoch(get_weekend())
        where_clause.append(
            "(completed >= ? AND completed <= ?)",
        )
        params.extend([mond, sund])
    elif today:
        today_val = get_deadline("today")
        where_clause.append(
            "(completed >= ? AND completed <= ?)",
        )
        params.extend(
            [convert_time_to_epoch(today_val, False), convert_time_to_epoch(today_val)],
        )
    elif date:
        where_clause.append(
            "(completed >= ? AND completed <= ?)",
        )
        params.extend([convert_time_to_epoch(date, False), convert_time_to_epoch(date)])

    if inprogress or completed or pending:
        clause = []
        if inprogress:
            clause.append("?")
            params.append(STATUS_IN_PROGRESS)
        if completed:
            clause.append("?")
            params.append(STATUS_COMPLETED)
        if pending:
            clause.append("?")
            params.append(STATUS_PENDING)
        where_clause.append("status in (" + ",".join(clause) + ")")
    else:
        clause = ["?", "?"]
        params.extend([STATUS_IN_PROGRESS, STATUS_PENDING])
        where_clause.append("status in (" + ",".join(clause) + ")")

    if priority:
        where_clause.append("priority = ?")
        params.append(priority)

    if label:
        where_clause.append("label = ?")
        params.append(label)

    where_clause_str = "WHERE " + " AND ".join(where_clause) if where_clause else ""

    try:
        results = database.list_table(
            table=table,
            columns=[
                "id",
                "title",
                "parent_id",
                "status",
                "deadline",
                "priority",
                "label",
                "description",
                "subtasks",
            ],
            where_clause=where_clause_str,
            params=tuple(params),
            order_by=f"ORDER BY {order_by}",
        )
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

    final_results = []
    for result in results:
        final_results.append(
            {
                "id": result[0],
                "title": result[1],
                "parent_id": result[2],
                "status": result[3],
                "deadline": (convert_epoch_to_date(result[4])),
                "priority": result[5],
                "label": result[6] if result[6] else "None",
                "description": result[7],
                "subtasks": result[8],
            },
        )
    return final_results


def add_tasks(
    title: str,
    table=DEFAULT_TABLE,
    description=None,
    priority=None,
    today=False,
    week=False,
    deadline=None,
    inprogress=None,
    completed=None,
    pending=None,
    label=None,
    parent=None,
):
    """
    Add a task to the database.
    """
    columns = ["title"]
    values = [title]
    if description:
        columns.append("description")
        values.append(description)
    if priority:
        columns.append("priority")
        values.append(priority)
    if today:
        columns.append("deadline")
        values.append(convert_time_to_epoch(get_deadline("today")))
    elif week:
        columns.append("deadline")
        values.append(convert_time_to_epoch(get_deadline("week")))
    elif deadline:
        columns.append("deadline")
        values.append(convert_time_to_epoch(deadline))
    if inprogress:
        columns.append("status")
        values.append(STATUS_IN_PROGRESS)
    elif completed:
        columns.append("status")
        values.append(STATUS_COMPLETED)
        columns.append("completed")
        values.append(convert_time_to_epoch(get_deadline("today")))
    elif pending:
        columns.append("status")
        values.append(STATUS_PENDING)
    if label:
        columns.append("label")
        values.append(label)
    if parent:
        columns.append("parent_id")
        values.append(parent["id"])
    try:
        database.insert_into_table(table, columns=columns, values=values)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return
    # Insert the record then increment the count of the parent task.
    if parent:
        parent_subtasks = parent.get("subtasks", 0) + 1
        database.update_table(
            table,
            {"subtasks": parent_subtasks, "id": parent["id"]},
        )


def search_task(task_id, table: str):
    """
    Search a task by its id.
    :param task_id:
    :return: task_details
    """
    try:
        task = database.list_table(
            table=table,
            columns=[
                "id",
                "title",
                "description",
                "status",
                "deadline",
                "priority",
                "label",
                "completed",
                "parent_id",
                "subtasks",
            ],
            where_clause="WHERE id = ?",
            params=(task_id,),
        )
    except sqlite3.Error:
        generate_migration_error()
        return None

    task_details = {}
    if task:
        task = task[0]
        task_details = {
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "status": task[3],
            "deadline": convert_epoch_to_date(task[4]),
            "priority": task[5],
            "label": task[6] if task[6] else "None",
            "completed": convert_epoch_to_date(task[7]),
            "parent_id": task[8],
            "subtasks": task[9],
        }
    return task_details


def get_subtasks(task_id: int, table: str):
    try:
        results = database.list_table(
            table=table,
            columns=[
                "id",
                "title",
                "status",
                "deadline",
                "priority",
                "label",
                "description",
                "subtasks",
                "parent_id",
            ],
            where_clause="WHERE parent_id = ?",
            params=(task_id,),
            order_by="ORDER BY completed ASC, status ASC, priority DESC",
        )
    except sqlite3.Error:
        generate_migration_error()
        return []
    final_results = []
    for result in results:
        final_results.append(
            {
                "id": result[0],
                "title": result[1],
                "status": result[2],
                "deadline": (convert_epoch_to_date(result[3])),
                "priority": result[4],
                "label": result[5] if result[5] else "None",
                "description": result[6],
                "subtasks": result[7],
                "parent_id": result[8],
            },
        )
    return final_results


def get_subtasks_recursive(task: dict, table: str):
    if task["subtasks"] == 0:
        return []

    try:
        all_subtasks = database.list_table(
            table=table,
            columns=[
                "id",
                "title",
                "status",
                "deadline",
                "priority",
                "label",
                "description",
                "subtasks",
                "parent_id",
            ],
            where_clause="WHERE parent_id IS NOT NULL",
            order_by="ORDER BY completed ASC, status ASC, priority DESC",
        )
    except sqlite3.Error:
        generate_migration_error()
        return []

    children_map = defaultdict(list)
    for row in all_subtasks:
        child_dict = {
            "id": row[0],
            "title": row[1],
            "status": row[2],
            "deadline": convert_epoch_to_date(row[3]),
            "priority": row[4],
            "label": row[5] if row[5] else "None",
            "description": row[6],
            "subtasks": row[7],
            "parent_id": row[8],
        }
        children_map[row[8]].append(child_dict)

    final_results = [task]

    def traverse(node_id):
        for child in children_map[node_id]:
            final_results.append(child)
            if child["subtasks"] > 0:
                traverse(child["id"])

    traverse(task["id"])
    return final_results


def update_task(updated_data: dict, table: str):
    """If marked as completed then set datetime as now else retain prev value"""

    updated_data["deadline"] = get_deadline(updated_data["deadline"])

    if updated_data["status"] == STATUS_COMPLETED:
        updated_data["completed"] = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    else:
        updated_data["completed"] = updated_data["deadline"]

    updated_data["deadline"] = convert_time_to_epoch(updated_data["deadline"])
    updated_data["completed"] = convert_time_to_epoch(updated_data["completed"])

    final_data = {}

    for key, value in updated_data.items():
        if value is None:
            continue
        final_data[key] = value

    try:
        database.update_table(table, final_data)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        generate_migration_error()
        return
    if updated_data["subtasks"] != 0 and updated_data["status"] == STATUS_COMPLETED:
        children = get_subtasks(updated_data["id"], table)
        for child in children:
            child["status"] = STATUS_COMPLETED
            try:
                update_task(child, table)
            except sqlite3.Error:
                generate_migration_error()


def handle_delete(current_task: dict, table: str):
    """
    Delete a task from the database
    """

    database.delete_task(table, current_task["id"])
    children = database.list_table(
        table=table,
        columns=["id", "parent_id"],
        where_clause="WHERE parent_id = ?",
        params=(current_task["id"],),
    )
    for child in children:
        handle_delete({"id": child[0], "parent_id": child[1]}, table)
    if current_task["parent_id"]:
        parent = search_task(current_task["parent_id"], table)
        if parent and parent["subtasks"] > 0:
            try:
                database.update_table(
                    table,
                    {
                        "subtasks": parent["subtasks"] - 1,
                        "id": current_task["parent_id"],
                    },
                )
            except sqlite3.Error as e:
                print(f"Database error: {e}")


def list_tables() -> list:
    """
    List all the tables in the database.
    """
    try:
        res = database.list_tables()
    except sqlite3.Error:
        generate_migration_error()
        return []

    result = []
    for table in res:
        if table[0] not in ("sqlite_sequence", "sessions", "session_data"):
            result.append(table[0])
    return result


def add_table(table_name: str) -> bool:
    """
    Add a table to the database.
    """
    try:
        database.initialize(table_name)
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def delete_table(table_name: str) -> bool:
    """
    Delete a table from the database.
    """
    try:
        database.delete_table(table_name)
        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def rename_table(old_name: str, new_name: str) -> bool:
    """
    Rename a table in the database.
    """
    try:
        database.rename_table(old_name, new_name)
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def get_deadline(deadline):
    if deadline == "week":
        deadline = str(get_weekend())
    elif deadline == "today":
        deadline = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    else:
        deadline = str(deadline)

    return deadline


def start_session(task_id: int, table: str, session_data: dict):
    """
    Start a session for a task.
    """
    # TODO: Write database calls
    if session_data.get("pid", 0) > 0:
        # If a session is already active, end it first
        end_session(session_data)
        display_info_message("A session was already active, ending it.")

    if get_os() == "Linux":
        try:
            pid, filehandle = linux_session_start()
            session_data["pid"] = pid
            session_data["file_handle"] = filehandle
        except Exception as e:
            display_error_message(f"Failed to start session: {e}")
            return None
    else:
        display_error_message("Session tracking is only supported on Linux.")
        return None

    # Start a new session
    session_data["start_time"] = int(datetime.datetime.now().timestamp())
    session_data["task_id"] = task_id
    session_data["table"] = table
    display_info_message("Session started.")
    return session_data


def end_session(session_data: dict):
    """
    End the current session.
    """
    if session_data.get("pid", 0) == 0:
        return

    data = {}

    if get_os() == "Linux":
        try:
            ok, err = linux_session_end(session_data["pid"])
            if not ok:
                if err is not None:
                    display_error_message(f"Failed to end session: {err}")
                return None
            with open(session_data["file_handle"], "r") as f:
                time.sleep(1)
                content = f.read().strip()
                if not content:
                    display_error_message("Session file is empty.")
                    return None
                data = json.loads(content)

        except Exception as e:
            display_error_message(f"Failed to end session: {e}")
            return None

    session_data["end_time"] = int(datetime.datetime.now().timestamp())

    try:
        session_id = database.add_session(
            task_id=session_data["task_id"],
            table_name=session_data["table"],
            start_datetime=session_data["start_time"],
            end_datetime=session_data["end_time"],
        )
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    session_data["session_id"] = session_id
    mapped_data = {}
    for value in data.values():
        if value["name_list"]:
            name = "-".join(value["name_list"])
            if mapped_data.get(name, None) is None:
                mapped_data[name] = value["time"]
            else:
                mapped_data[name] += value["time"]
    for key, value in mapped_data.items():
        try:
            database.add_session_data(
                session_id=session_id,
                application_name=key,
                duration=value,
            )
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    return {"session_id": session_id, "session_data": session_data}


def list_sessions(table: str, task_id: int = None) -> list:
    """
    List all the sessions, filter by task_id.
    """
    try:
        sessions = database.list_sessions(table, task_id)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

    session_list = []

    for session in sessions:
        task = search_task(session[1], table)
        duration = session[4] - session[3]
        if duration < 0:
            duration = 0

        session_list.append(
            {
                "session_id": session[0],
                "task_name": task["title"],
                "start_datetime": convert_epoch_to_datetime(session[3]),
                "end_datetime": convert_epoch_to_datetime(session[4]),
                "duration": convert_seconds_delta_to_time(duration),
            },
        )

    return session_list


def get_session_data(session_id: int) -> dict:
    """
    Get session data for a given session ID.
    """
    try:
        session_data = database.get_session_data(session_id)
        data = {
            "data": [],
        }
        for session_item in session_data:
            data["data"].append(
                {
                    "application_name": session_item[2],
                    "duration": convert_seconds_delta_to_time(session_item[3]),
                },
            )
        return data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {}


def delete_session(session_id: int) -> bool:
    """
    Delete a session by its ID.
    """
    try:
        database.delete_session(session_id)
        return True
    except sqlite3.Error as e:
        display_error_message(f"Failed to delete session: {e}")
        return False
