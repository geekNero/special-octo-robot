import click
import os
import json
from app.database import initialize
from app.application import print_tasks

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


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
@click.option('-ls', '--list', is_flag=True, help='List all the tasks')
@click.option('-a', '--add', help='Add a new task', type=str)
def tasks(ctx, list, add):
    """
    Create, Modify, Delete and List as well as view specific tasks.
    """
    if list:
        pass
    elif add:
        task_list = ctx.obj['data']['tasks']
        task_list.append({
            'task': {
                'id': len(task_list) + 1,
                'title': add,
                'status': 'Pending',
                'deadline': 'No Deadline',
                'priority': 5,
            }
        })
        path = os.path.join(os.getenv("HOME"), ".devcord", "data.json")
        with open(path, "w") as f:
            json.dump(ctx.obj['data'], f)
