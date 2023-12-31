from rich.console import Console
from rich.table import Table


def get_status_color(task):
    if task["status"] == "In Progress":
        return "cyan"
    elif task["status"] == "Completed":
        return "green"
    elif task["status"] == "Pending":
        return "red"
    else:
        return "white"


def get_title_color(task):
    if task["priority"] == 6:
        return "rgb(255,82,82)"
    elif task["priority"] == 5:
        return "rgb(255,186,186)"
    elif task["priority"] == 4:
        return "rgb(190,41,236)"
    elif task["priority"] == 3:
        return "rgb(239,187,255)"
    elif task["priority"] == 2:
        return "blue"
    elif task["priority"] == 1:
        return "rgb(0,128,128)"
    else:
        return "rgb(153,122,141)"


def print_tasks(tasks):
    table = Table(title="Tasks")
    table.add_column("ID", justify="center", style="white", no_wrap=True)
    table.add_column("Task", justify="center", style="white")
    table.add_column("Status", justify="center", style="white")
    table.add_column("Deadline", justify="center", style="white")
    table.add_column("Subtasks", justify="center", style="white")

    for task in tasks:
        task = task["task"]
        print(task['priority'])
        table.add_row(
            str(task["id"]),
            f'[{get_title_color(task)}]'+task["title"],
            f'[{get_status_color(task)}]'+task["status"],
            task["deadline"],
            str(len(task["subtasks"])),
        )

    console = Console()
    console.print(table)
