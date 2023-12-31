import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.argument('-l', '--list', is_flag=True, help='List all the tasks')
def tasks(list):
    """
    Create, Modify, Delete and List all your tasks with parameters such as deadline, priority, etc.
    """
    if list:
        click.echo('Listing all the tasks')