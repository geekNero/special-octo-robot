import datetime

from click import echo
from click import style
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.completion import ThreadedCompleter

from app import application
from app.config import update_config
from app.constants import config_path


def convert_to_console_date(date_str, title=None):
    """
    Convert date from "YYYY-MM-DD" to "dd/mm/yyyy"
    """
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")


def convert_to_db_date(date_str):
    # Convert date from "dd/mm/yyyy" to "YYYY-MM-DD"
    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    return date_obj.strftime("%Y-%m-%d")


def sanitize_text(text):
    return text.strip().replace("'", '"')


def fuzzy_search_task(table, completed=False, current_task_id=-1):
    current_task_title = application.search_task(current_task_id, table).get(
        "title",
        "No Title",
    )

    if current_task_id == -1:  # root level
        tasks = application.list_tasks(table, subtasks=False, completed=completed)
    else:
        tasks = application.get_subtasks(
            current_task_id,
            table,
        )  # subtasks of current task

    if tasks is None:
        # previously selected task was leaf node and has no subtasks

        select_task_title = prompt(
            f"Currently Selected Task : {current_task_title}\nEnter . To select current task or Press Enter to go back one level\n",
        )
        if select_task_title.strip() == ".":
            return current_task_id
        return fuzzy_search_task(
            table,
            completed,
            application.search_task(current_task_id, table).get("parent_id", -1),
        )

    task_titles = [each_task["title"] for each_task in tasks]
    task_completer = ThreadedCompleter(FuzzyWordCompleter(task_titles))
    select_task_title = prompt(
        f"Currently Selected Task : {current_task_title}\nEnter any part from title of the task OR press enter to go back one level OR . to quit\n",
        completer=task_completer,
    )

    if select_task_title.strip() == ".":
        if current_task_id == -1:
            return fuzzy_search_task(
                table,
                completed,
                current_task_id,
            )  # search continues
        return current_task_id

    if select_task_title.strip() == "":
        # user pressed enter without selecting any task
        parent_task = application.search_task(current_task_id, table).get(
            "parent_id",
        )
        if parent_task is None:
            parent_task = -1

        return fuzzy_search_task(table, completed, parent_task)

    current_task = next(
        (each_task for each_task in tasks if each_task["title"] == select_task_title),
        None,
    )

    if current_task is not None and current_task.get("subtasks", 0):
        return fuzzy_search_task(table, completed, current_task["id"])
    return current_task["id"]  # if leaf task


def generate_migration_error():
    echo(
        style(
            "Have You Run Migrations? Run 'devcord init --migrate' to run migrations",
            fg="red",
        ),
    )


def sanitize_table_name(table_name: str) -> (str, bool):
    for ch in table_name:
        if ch.isalnum() or ch == " " or ch == "_":
            continue
        else:
            return "", False

    return table_name.replace(" ", "_"), True


def check_table_exists(table_name: str) -> bool:
    table_name, ok = sanitize_table_name(table_name)
    if not ok:
        echo(
            style(
                "Error: Table name is not valid, please use only alphanumeric characters or underscores."
                + "Maybe you are not a developer?",
                fg="red",
            ),
        )
    return table_name in application.list_tables(), table_name
