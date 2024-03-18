from rich.console import Console
from rich.table import Table


def get_style_color(task):
    if task["priority"] == 5:
        return "#FF0000"
    elif task["priority"] == 4:
        return "red"
    elif task["priority"] == 3:
        return "yellow"
    elif task["priority"] == 2:
        return "#3B9EBF"
    elif task["priority"] == 1:
        return "#ADD8E6"
    else:
        return "#FFFFFF"


def print_tasks(tasks):
    table = Table(title="Tasks")
    table.add_column("ID", justify="center", style="white", no_wrap=True)
    table.add_column("Task", justify="center", style="white")
    table.add_column("Status", justify="center", style="white")
    table.add_column("Deadline", justify="center", style="white")
    table.add_column("Label", justify="center", style="white")

    for task in tasks:
        table.add_row(
            str(task["id"]),
            task["title"],
            task["status"],
            task["deadline"],
            task["label"],
            style=f"{get_style_color(task)}",
        )

    console = Console()
    console.print(table)
