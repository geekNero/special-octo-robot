import click
import os
import json

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """
    Devcord is a CLI tool for developers to help them with their daily tasks.
    """
    ctx.ensure_object(dict)
    path = os.path.join(os.getenv("HOME"), ".devcord", "data.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        folder_path = os.path.join(os.getenv("HOME"), ".devcord")
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        with open(path, "w+") as f:
            data = {
                'tasks': [],
            }
            json.dump(data, f)

    ctx.obj['data'] = data


@cli.command()
@click.pass_context
@click.option('-l', '--list', is_flag=True, help='List all the tasks')
def tasks(ctx, list):
    """
    Create, Modify, Delete and List all your tasks with parameters such as deadline, priority, etc.
    """
    if list:
        task_list = ctx.obj['data']['tasks']
        counter = 1
        for task in task_list:
            click.echo(f'{counter}. {task["task"]["short_description"]}')
            counter += 1
        if counter == 1:
            click.echo("No tasks found.")
