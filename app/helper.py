from click import echo
from click import style
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.completion import ThreadedCompleter

from app import application
from app.utility import sanitize_table_name


def fuzzy_search_task(table, completed=False, current_task_id=-1):
    current_task = (
        application.search_task(current_task_id, table) if current_task_id > 0 else {}
    )
    current_task_title = current_task.get(
        "title",
        "Root",
    )

    if current_task_id == -1:  # root level
        tasks = application.list_tasks(table, subtasks=False, completed=completed)
    else:
        tasks = application.get_subtasks(
            current_task_id,
            table,
        )  # subtasks of current task

    task_titles = [each_task["title"] for each_task in tasks]
    task_completer = ThreadedCompleter(FuzzyWordCompleter(task_titles))
    if len(current_task_title) > 30:
        current_task_title = current_task_title[:30] + "..."
    select_task_title = prompt(
        f"\nCurrently selected Task : {current_task_title}, "
        + "press: \nAny part of the title, OR\nPress ↵ to go back one level, OR\nPress . to select current task\n\n",
        completer=task_completer,
    )

    if select_task_title.strip() == ".":
        if current_task_id == -1:
            echo(
                style(
                    "Error: Cannot select root task.",
                    fg="red",
                ),
            )
        else:
            return current_task

    elif select_task_title.strip() == "":
        # user pressed enter without selecting any task
        parent_task_id = current_task.get(
            "parent_id",
        )

        current_task_id = parent_task_id if parent_task_id is not None else -1

    else:
        current_task = next(
            (
                each_task
                for each_task in tasks
                if each_task["title"] == select_task_title
            ),
            None,
        )
        if current_task == None:
            echo(
                style(
                    "Error: Task not found. Please select a valid task",
                    fg="red",
                ),
            )
        else:
            current_task_id = current_task["id"]

    return fuzzy_search_task(table, completed, current_task_id)  # if leaf task


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
