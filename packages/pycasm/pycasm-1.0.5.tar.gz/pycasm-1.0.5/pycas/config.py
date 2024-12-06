from __future__ import annotations

import argparse
from argparse import Namespace
import importlib
import sys
import yaml
from pycas.logger import log

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    Module = importlib.util.types.ModuleType


__config_file__ = "pycas.yml"


def parse_cli():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-ck", "--cookie", type=str, help="give the cookie of pycas"
        )
        parser.add_argument("-tk", "--token", type=str, help="give the token of pycas")
        parser.add_argument(
            "-p", "--page", type=int, help="give the start page", default=1
        )
        parser.add_argument(
            "-s", "--size", type=int, help="give the page size", default=100
        )
        parser.add_argument(
            "--config_file",
            help="Path to the custom configuration file",
        )
        parser.add_argument(
            "-v", "--version", action="store_true", help="Display the version of pycas"
        )
        parser.add_argument(
            "--log-level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Level of messages to Display, can be DEBUG / INFO / WARNING / ERROR / CRITICAL",
        )
        args = parser.parse_args()
        return args
    except argparse.ArgumentError as err:
        log.error(str(err))
        sys.exit(2)


def get_custom_config():
    global __config_file__

    with open(__config_file__, "r") as file:
        custom_config = yaml.safe_load(file)

    return custom_config


def get_configuration(args: Namespace) -> dict:
    custom_config = get_custom_config()

    return {
        "cookie": custom_config["cookie"],
        "token": custom_config["token"],
    }
