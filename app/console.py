import json
import os

from click import echo
from click import style
from rich.console import Console
from rich.style import Style
from rich.table import Table


def get_priority_color(priority):
    if priority == 5:
        return "bold red"
    elif priority == 4:
        return "#EE4B2B"
    elif priority == 3:
        return "magenta"
    elif priority == 2:
        return "blue"
    elif priority == 1:
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


def get_table(tasks, plain=False):
    table = Table(title="Tasks", highlight=True, leading=True)
    table.add_column("Priority", justify="center", style="white")
    table.add_column("Task", justify="left", style="white")
    table.add_column("Status", justify="center", style="white")
    table.add_column("Deadline", justify="center", style="white")
    table.add_column("Label", justify="center", style="white")
    table.add_column("ID", justify="center", style="white", no_wrap=True)
    table.add_column("Properties", justify="center", style="white")
    text_style = Style(color="#FFFFFF")
    bold_text_style = Style(color="#FFFFFF", bold=True)
    none_style = Style(color="magenta")
    for task in tasks:
        properties = []
        if task["description"] and task["description"] not in [
            "None",
            "No given description",
        ]:
            if plain:
                properties.append("Description")
            else:
                properties.append("►")
        if task["subtasks"] > 0:
            if plain:
                properties.append("Subtasks")
            else:
                properties.append("|☰")

        table.add_row(
            (
                f"[{get_priority_color(task['priority'])}]●"
                if not plain
                else f"[{text_style}]{task['priority']}"
            ),
            f'[{text_style}]{task["title"]}',
            f'[{get_status_color(task["status"])}][italic]{task["status"]}',
            task["deadline"],
            f'[{bold_text_style if task["label"] != "None" else none_style}]{task["label"]}',
            f"[{text_style}]{task['id']}",
            f"[{text_style}]{','.join(properties)}",
        )
    return table


def sanitize_path(path):
    if path[-1] == "/":
        echo(
            style(
                text="Error: Path is a directory, please provide a file path.",
                fg="red",
            ),
        )
        return False
    if not os.path.exists(os.path.dirname(path)):
        echo(
            style(
                text="Error: The directory where you are trying to store the file in does not exist.",
                fg="red",
            ),
        )
        return False
    return True


def print_tasks(tasks, output=None, path=None, plain=False):

    file = None
    if path:
        path = path.strip()
        if path[0] != "/":  # If path is not absolute
            path = os.path.join(os.getcwd(), path)

        if not sanitize_path(path):
            return

        file = open(path, "w+")
        console = Console(file=file)
    else:
        console = Console()

    if path:
        plain = True
    if output == "json":
        result = json.dumps(tasks, indent=4)
        console.print_json(result)

    elif output == "text":
        console.print("[bold]Tasks")
        console.rule()
        index = 1
        for task in tasks:
            console.print(
                f"{index}) Title: {task['title']}\n- Description: {task['description']}\n- Deadline: {task['deadline']}\n",
            )
            index += 1

    else:
        result = get_table(tasks, plain)
        console.print(result)

    if file:
        file.close()


def print_legend():
    text_style = Style(color="#FFFFFF")
    console = Console()
    table = Table(title="Priority Legend", highlight=True, leading=True)
    table.add_column("Unicode Character", justify="center", style="white")
    table.add_column("Value", justify="center", style="white")
    table.add_row(f"[{get_priority_color(0)}]●", f"[{text_style}]No Priority Level")
    for i in range(1, 6):
        table.add_row(
            f"[{get_priority_color(i)}]●",
            f"[{text_style}]Priority level: {i}",
        )
    console.print(table)
    console.rule()
    table = Table(title="Task Properties Legend", highlight=True, leading=True)
    table.add_column("Unicode Character", justify="center", style="white")
    table.add_column("Value", justify="center", style="white")
    table.add_row("[#FFFFFF]►", f"[{text_style}]Has description")
    table.add_row("[#FFFFFF]|☰", f"[{text_style}]Has subtasks")
    console.print(table)
