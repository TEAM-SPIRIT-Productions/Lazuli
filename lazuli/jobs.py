"""Contains the mapping for Job IDs to canonical names

This module looks for a `jobs.yaml` file in the package, and parses it into a
Python dictionary named `JOBS`. This can be thought of as a non-lazy instantiated singleton.
Note that if this file cannot be located, an exception is raised. The YAML 
file used is the same as the one maintained by Team SPIRIT: 
https://github.com/TEAM-SPIRIT-Productions/MapleStoryJobIDs

See the parser docs here:
https://yaml.readthedocs.io/en/latest/index.html
"""
from importlib.abc import Traversable
import importlib.resources
from pathlib import Path

from ruamel.yaml import YAML


def get_yaml_file(file_name: str) -> Traversable:
    # Note: `importlib.resources.files` will only work when lazuli is imported as a package
    package_files = importlib.resources.files("lazuli")
    yaml_file = package_files.joinpath(file_name)
    if yaml_file.is_file():
        return yaml_file
    raise FileNotFoundError(f"[{file_name}] should be placed in the root of the package!")


def parse_yaml_file(file_name: str) -> dict:
    # Create YAML parser object
    yaml = YAML(typ="safe", pure=True)
    
    with open(get_yaml_file(file_name), "r", encoding="utf-8") as yaml_file:
        contents = yaml.load(yaml_file)
        if contents is None:
            raise ValueError(f"[{file_name}] contents could not be read!")
    return contents


YAML_FILE_NAME = "jobs.yaml"
JOBS: dict[str, str] = parse_yaml_file(YAML_FILE_NAME)
print(JOBS)
