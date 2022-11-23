import re
from pprint import pprint
from typing import Optional
import json
import yaml
import toml
import os

OS = "macosx"

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


def parse_html(file):
    re_hou = r"houdini(-|-py\d+-)(\d+)\.(\d+)\.(\d+)-([a-z0-9]+).+\.(dmg|tar\.gz|exe)"
    re_dck = r"Houdini(\d+)\.(\d+)\.(\d+)_Docker\.zip"
    re_lbs = r"SideFXLabs(\d+)\.(\d+)\.(\d+)\.zip"

    data = {}

    current_heading = None
    current_subheading = None

    for i, row in enumerate(file):

        row = row.strip()

        if row in HEADINGS:
            current_heading = row.replace(" ", "_")
            data[current_heading] = {}

        if row in SUBHEADINGS and current_heading in data:
            current_subheading = row.replace(" ", "_").replace(".", "_")
            data[current_heading][current_subheading] = []

        if re.search(re_hou, row) or re.search(re_dck, row) or re.search(re_lbs, row):
            data[current_heading][current_subheading].append(row)

    return data


def dump(data, filename, method="json"):

    os.mkdir("../json") if not os.path.isdir("../json") else None
    os.mkdir("../yaml") if not os.path.isdir("../yaml") else None
    os.mkdir("../toml") if not os.path.isdir("../toml") else None

    if method.lower() in ("json", "j"):
        with open(f"../json/{filename}.json", "w") as fp:
            json.dump(data, fp, indent=4)
    elif method.lower() in ("yaml", "y"):
        with open(f"../yaml/{filename}.yaml", "w") as fp:
            yaml.dump(data, fp)
    elif method.lower() in ("toml", "t"):
        with open(f"../toml/{filename}.toml", "w") as fp:
            toml.dump(data, fp)


def main():

    with open("../html/Daily Builds SideFX.html") as fp:
        data = parse_html(fp)

    dump(data, "test", method="j")
    dump(data, "test", method="y")
    dump(data, "test", method="t")

    # for line in html:

    # houdini_all = re.findall(r'<a href=".+">\n.+(houdini-.+\..+)\n.+</a>', html)

    # regex = (
    #     r"houdini(-|-py\d+-)(\d+\.\d+\.\d+)-(macosx|linux|win64).+\.(dmg|tar\.gz|exe)"
    # )

    # for ver in houdini_all:
    #     match = re.search(regex, ver)
    #     file = match.group()
    #     python, version, os, _ = match.groups()
    #     python = (
    #         None
    #         if python == "-"
    #         else float(python.removeprefix("-py").removesuffix("-").ljust(4, "0"))
    #         * 0.001
    #     )
    #     major, minor, patch = [int(x) for x in version.split(".")]
    #     # python = fmt_pyver(python)
    #     # print(python)

    #     if os == "macosx" and major == 19 and python == 3.7:
    #         print(f"houdini-{version}")


if __name__ == "__main__":
    main()
