import os
import subprocess
from glob import glob

from iterfzf import iterfzf


paths = [
    "~/Downloads/",
    "~/dev/",
    "~/dev/*/",
    "~/dev/gdev/*/",
    "~/dev/home/*/",
    "~/dev/work/*/",
    "~/dev/ref/*/",
]


home_path = os.path.expanduser(os.path.normpath("~/"))

all_paths = []


for p in paths:
    p = os.path.normpath(p)
    p = os.path.expanduser(p)
    if "*" in p:
        all_paths.extend(
            "~" + i.removeprefix(home_path) for i in
            glob(p, recursive=True, include_hidden=True)
        )
    else:
        p = "~" + p.removeprefix(home_path)
        all_paths.append(p)

all_paths.sort()

a = iterfzf(all_paths)

if a is not None:
    directory = os.path.expanduser(a)
    command = "start neovide.exe ."
    print(directory, command)
    subprocess.call(command, cwd=directory, shell=True)
