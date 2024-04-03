from rich.console import Console
from rich.style import Style
from rich.table import Table


def get_priority_color(task):
    if task["priority"] == 5:
        return "bold red"
    elif task["priority"] == 4:
        return "#EE4B2B"
    elif task["priority"] == 3:
        return "magenta"
    elif task["priority"] == 2:
        return "blue"
    elif task["priority"] == 1:
        return "cyan"
    else:
        return "#FFFFFF"


def get_status_color(status):
    if status == "Completed":
        return "#50C878"
    elif status == "Pending":
        return "bold red"
    else:
        return "#FFFFFF"


def print_tasks(tasks):
    table = Table(title="Tasks", highlight=True, leading=True)
    table.add_column("Priority", justify="center", style="white")
    table.add_column("Task", justify="left", style="white")
    table.add_column("Status", justify="center", style="white")
    table.add_column("Deadline", justify="center", style="white")
    table.add_column("Label", justify="center", style="white")
    table.add_column("ID", justify="center", style="white", no_wrap=True)

    text_style = Style(color="#FFFFFF")
    bold_text_style = Style(color="#FFFFFF", bold=True)
    none_style = Style(color="magenta")

    for task in tasks:
        table.add_row(
            f"[{get_priority_color(task)}]●",
            f'[{text_style}]{task["title"]}',
            f'[{get_status_color(task["status"])}][italic]{task["status"]}',
            task["deadline"],
            f'[{bold_text_style if task["label"]!="None" else none_style}]{task["label"]}',
            f"[{text_style}]{task['id']}",
        )

    console = Console()
    console.print(table)
