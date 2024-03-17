import json
import os

import click

import app.application as application
from app.console import print_tasks
from app.database import initialize

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """
    Devcord is a CLI tool for developers to help them with their daily tasks.
    """
    ctx.ensure_object(dict)
    path = os.path.join(os.getenv("HOME"), ".devcord", "data.db")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        initialize()


@cli.command()
@click.pass_context
@click.option("-l", "--list", is_flag=True, help="List all the tasks")
@click.option("-a", "--add", help="Add a new task", type=str)
@click.option("-p", "--priority", help="Set the priority of a task", type=int)
@click.option("-t", "--today", is_flag=True, help="Perform for all the tasks for today")
@click.option(
    "-w",
    "--week",
    is_flag=True,
    help="Perform for  all the tasks for this week",
)
@click.option(
    "-i",
    "--inprogress",
    is_flag=True,
    help="Perform for all the tasks that are in progress",
)
@click.option(
    "-c",
    "--completed",
    is_flag=True,
    help="Perform for all the tasks that are completed",
)
@click.option(
    "-pd",
    "--pending",
    is_flag=True,
    help="Perform for all the tasks that are pending",
)
def tasks(
    ctx,
    list=None,
    add=None,
    priority=None,
    today=None,
    week=None,
    inprogress=None,
    completed=None,
    pending=None,
):
    """
    Create, Modify, Delete and List as well as view specific tasks.
    """
    if list:
        print_tasks(
            application.list_tasks(
                priority=priority,
                today=today,
                week=week,
                inprogress=inprogress,
                completed=completed,
                pending=pending,
            ),
        )
    elif add:
        task_list = ctx.obj["data"]["tasks"]
        task_list.append(
            {
                "task": {
                    "id": len(task_list) + 1,
                    "title": add,
                    "status": "Pending",
                    "deadline": "No Deadline",
                    "priority": 5,
                },
            },
        )
        path = os.path.join(os.getenv("HOME"), ".devcord", "data.json")
        with open(path, "w") as f:
            json.dump(ctx.obj["data"], f)
