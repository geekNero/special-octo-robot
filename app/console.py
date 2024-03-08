from rich.console import Console
from rich.table import Table


def get_style_color(task):
    if task["priority"] == 5:
        return "red"
    elif task["priority"] == 4:
        return "orange"
    elif task["priority"] == 3:
        return "yellow"
    elif task["priority"] == 2:
        return "rgb(173, 216, 230)"
    elif task["priority"] == 1:
        return "rgb(221, 221, 221)"
    else:
        return "white"


def print_tasks(tasks):
    table = Table(title="Tasks")
    table.add_column("ID", justify="center", style="white", no_wrap=True)
    table.add_column("Task", justify="center", style="white")
    table.add_column("Status", justify="center", style="white")
    table.add_column("Deadline", justify="center", style="white")

    for task in tasks:
        task = task["task"]
        print(task['priority'])
        table.add_row(
            str(task["id"]),
            task["title"],
            task["status"],
            task["deadline"],
            style=f'{get_style_color(task)}',
        )

    console = Console()
    console.print(table)
