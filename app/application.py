from rich.console import Console
from rich.table import Table


def get_style_color(task):
    if task["priority"] == 6:
        return "rgb(255,82,82)"
    elif task["priority"] == 5:
        return "rgb(255,186,186)"
    elif task["priority"] == 4:
        return "yellow"
    elif task["priority"] == 3:
        return "green"
    elif task["priority"] == 2:
        return "cyan"
    elif task["priority"] == 1:
        return "blue"
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
            task["title"],
            task["status"],
            task["deadline"],
            str(len(task["subtasks"])),
            style=f'{get_style_color(task)}',
        )

    console = Console()
    console.print(table)
