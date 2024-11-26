import json
import sys

from .__version__ import VERSION


def check_unicode_support():
    return sys.stdout.encoding.lower() in ("utf-8", "utf-16", "utf-32")


def initialize_config(
    path,
    theme="light",
    default_output="table",
    version=VERSION,
    pretty_tree=True,
    current_table="tasks",
    **kwargs,
):
    with open(path, "w+") as file:
        config = {
            "theme": theme,
            "default_output": default_output,
            "version": version,
            "pretty_tree": pretty_tree,
            "current_table": current_table,
        }
        json.dump(config, file, indent=4)
        return config


def update_config(path, config):
    initialize_config(path, **config)


def get_config(path):
    with open(path, "r") as file:
        return json.load(file)
