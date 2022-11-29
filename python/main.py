import re
import os
import json

# Typing
from typing import TextIO

HEADINGS = {f"Houdini {x}" for x in {"19.5", "19.0", "18.5", "18.0", "17.5", "17.0"}}

SUBHEADINGS = {
    "Production Builds",
    "Daily Builds",
    "Daily Builds - Python 3.7",
    "SideFX Labs",
    "Docker",
    "Apple Silicon Builds Tech Preview",
    "Production Builds - Python 3",
}

# RegEx
REGEX_HOUDINI_FILE = (
    r"houdini(-|-py\d+-)((\d+)\.(\d+)\.(\d+))-([a-z0-9]+).+\.(dmg|tar\.gz|exe)"
)
REGEX_DOCKER_FILE = r"Houdini((\d+)\.(\d+)\.(\d+))_Docker\.zip"
REGEX_SIDEFXLABS_FILE = r"SideFXLabs((\d+)\.(\d+)\.(\d+))\.zip"


def parse_html(html: TextIO) -> dict:
    data: dict = {}

    current_heading = None
    current_subheading = None

    for i, row in enumerate(html):

        row = row.strip()

        if row in HEADINGS:
            current_heading = row.replace(" ", "_")
            data[current_heading] = {}
            continue

        if row in SUBHEADINGS and current_heading in data:
            current_subheading = row.replace(" ", "_").replace(".", "_")
            data[current_heading][current_subheading] = []
            continue

        if re.search(REGEX_HOUDINI_FILE, row):
            data[current_heading][current_subheading].append(houdini(row))
        elif re.search(REGEX_DOCKER_FILE, row):
            data[current_heading][current_subheading].append(docker(row))
        elif re.search(REGEX_SIDEFXLABS_FILE, row):
            data[current_heading][current_subheading].append(sidefxlabs(row))

    return data


def houdini(file: str, expand_version=False) -> dict:
    match = re.search(REGEX_HOUDINI_FILE, file)
    python, version, major, minor, patch, platform, _ = match.groups()

    python = (
        None
        if python == "-"
        else float(re.search(r"-py(\d+)-", python).group(1).ljust(2, "0")) * 0.1
    )
    if expand_version:
        version = _expand_version(version, major, minor, patch)

    return {"version": version, "python": python, "platform": platform, "file": file}


def docker(file: str, expand_version=False) -> dict:
    match = re.search(REGEX_DOCKER_FILE, file)
    ver, major, minor, patch = match.groups()
    ver = _expand_version(ver, major, minor, patch) if expand_version else ver
    return {"version": ver, "file": file}


def sidefxlabs(file: str, expand_version=False) -> dict:
    match = re.search(REGEX_SIDEFXLABS_FILE, file)
    ver, major, minor, patch = match.groups()
    ver = _expand_version(ver, major, minor, patch) if expand_version else ver
    return {"version": ver, "file": file}


def _expand_version(version, major, minor, patch):
    major, minor, patch = (int(x) for x in (major, minor, patch))
    return {"version": version, "major": major, "minor": minor, "patch": patch}


def dump(data: dict, filename: str) -> None:

    directory = os.path.join("..", "json")
    os.mkdir(directory) if not os.path.isdir(directory) else None
    file = filename + "." + "json"
    path = os.path.join(directory, file)

    with open(path, "w") as fp:
        json.dump(data, fp, indent=4)


def main():

    with open("../html/Daily Builds SideFX.html") as fp:
        data = parse_html(fp)

    dump(data, "builds")


if __name__ == "__main__":
    main()
