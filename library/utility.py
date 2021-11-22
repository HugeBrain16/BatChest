"""utility library for the bot"""

import os
import importlib
from typing import List
from cmdtools.ext.command import CommandWrapper


def mention_to_id(mention: str) -> int:
    """extract user id from discord mention"""
    result = 0

    try:
        result = int(
            mention.replace("<", "").replace(">", "").replace("!", "").replace("@", "")
        )
    except (AttributeError, ValueError):
        pass

    return result


def load_command(name: str):
    """load commands from library"""
    for file in os.listdir("library/commands"):
        if file.endswith(".py") and os.path.isfile("library/commands/" + file):
            modname = file.rsplit(".py", 1)[0]
            modpath = os.path.join("library", "commands", modname).replace(os.sep, ".")
            mod = importlib.import_module(modpath)

            if hasattr(mod, "group") and name == modname:
                return mod if isinstance(mod.group, CommandWrapper) else None


def get_commands() -> List[str]:
    """get command names from library"""
    cmds = []

    for file in os.listdir("library/commands"):
        if file.endswith(".py") and os.path.isfile("library/commands/" + file):
            modname = file.rsplit(".py", 1)[0]
            mod = load_command(modname)

            if mod:
                cmds.append(modname)

    return cmds
