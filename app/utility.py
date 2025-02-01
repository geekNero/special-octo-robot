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


def fuzzy_search_task(table, completed=False, current_task_id=-1, ctx={}) -> dict:

    def search_task_recur(tasks, table):
        task_titles = [each_task["title"] for each_task in tasks]
        task_completer = ThreadedCompleter(FuzzyWordCompleter(task_titles))
        select_task_title = prompt(
            "Enter any part from title of the task OR -1 to go back one level\n",
            completer=task_completer,
        )

        # go back one level
        if select_task_title.strip() == "-1":
            return -1

        current_task = next(
            (
                each_task
                for each_task in tasks
                if each_task["title"] == select_task_title
            ),
            None,
        )

        if current_task is not None and current_task.get("subtasks", 0):
            proceed = (
                prompt("Do you want to search within the subtasks? (y/n): ")
                .strip()
                .lower()
            )
            if proceed == "y":
                val = search_task_recur(
                    application.get_subtasks(current_task["id"], table),
                    table,
                )
                if val == -1:
                    return search_task_recur(tasks, table)
                return val
        return current_task

    if current_task_id == -1:  # if -1 then list tasks from root level
        all_tasks = application.list_tasks(table, subtasks=False, completed=completed)
    else:
        all_tasks = application.get_subtasks(
            current_task_id,
            table,
        )  # if not -1 then list subtasks of current task

    task = search_task_recur(all_tasks, table)  # proceed with the search

    copy_of_current_task = current_task_id
    while (
        task == -1
    ):  # already at root position or user wants to go back from any node to parent node.
        copy_of_current_task = application.search_task(copy_of_current_task, table).get(
            "parent_id",
        )
        if copy_of_current_task is None:
            all_tasks = application.list_tasks(
                table,
                subtasks=False,
                completed=completed,
            )
            copy_of_current_task = -1  # came back to root level so mark it as -1
        else:
            all_tasks = application.get_subtasks(copy_of_current_task, table)
        task = search_task_recur(all_tasks, table)

    if task is not None and task["id"] != current_task_id:
        ctx.obj["config"]["current_task"] = task["id"]
        update_config(config_path, ctx.obj["config"])

    return task


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
