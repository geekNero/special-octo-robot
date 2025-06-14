import sqlite3

from packaging.version import Version

from .constants import db_path
from app.__version__ import VERSION
from app.config import update_config
from app.constants import config_path
from app.db_upgrade import upgrades


migration_list = [
    ("0.5.1", "", upgrades.upgrade_0_5_1),
    ("0.6.3", "", upgrades.upgrade_0_6_3),
    ("1.0.0", "", upgrades.upgrade_1_0_0),
]


def run_migrations(previous_version):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    previous_version = Version(previous_version)
    for migration in migration_list:
        if Version(migration[0]) > previous_version:
            migration[2](cur)
    conn.commit()
    conn.close()


def update_version(config):
    if config["version"] != VERSION:
        run_migrations(previous_version=config["version"])
        config["version"] = VERSION
        update_config(config_path, config=config)
