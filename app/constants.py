import os
import platform

from click import echo
from click import style


if platform.system() == "Windows":
    home_word_list = ["USERPROFILE", "HOMEDRIVE", "HOMEPATH"]
    for home_word in home_word_list:
        if home_word in os.environ:
            path = os.path.join(os.environ[home_word], ".devcord")
            break
    else:
        path = None
else:
    path = os.path.join(os.getenv("HOME"), ".devcord")

if path:
    db_path = os.path.join(path, "data.db")
    config_path = os.path.join(path, "config.json")
else:
    db_path = None
    config_path = None
