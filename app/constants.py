import os
import platform


if platform.system() == "Windows":
    home_word_list = ["USERPROFILE", "HOMEDRIVE", "HOMEPATH"]
    for home_word in home_word_list:
        if home_word in os.environ:
            path = os.path.join(os.environ[home_word], ".devcord")
            break
    else:
        path = None
else:
    # Path value can be None as there is a check in devcord.py
    home = os.getenv("HOME")
    if home is not None:
        path = os.path.join(home, ".devcord")

if path:
    if os.environ.get("DEBUG", "") == "True":
        db_path = os.path.join(path, "test.db")
        config_path = os.path.join(path, "test_config.json")
    else:
        db_path = os.path.join(path, "data.db")
        config_path = os.path.join(path, "config.json")
else:
    db_path = ""
    config_path = ""

LF_ENTER = 10
CR_ENTER = 13
