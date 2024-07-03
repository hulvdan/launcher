import os
import subprocess
from glob import glob

from iterfzf import iterfzf


HOME_PATH = os.path.expanduser(os.path.normpath("~/"))

PATHS = [
    "~/Downloads/",
    "~/dev/",
    "~/dev/*/",
    "~/dev/gdev/*/",
    "~/dev/home/*/",
    "~/dev/work/*/",
    "~/dev/ref/*/",
]


def main() -> None:
    all_paths = []

    for p in PATHS:
        p = os.path.normpath(p)
        p = os.path.expanduser(p)
        if "*" in p:
            all_paths.extend(
                "~" + i.removeprefix(HOME_PATH)
                for i in glob(p, recursive=True, include_hidden=True)
            )
        else:
            p = "~" + p.removeprefix(HOME_PATH)
            all_paths.append(p)

    selected_path = iterfzf(sorted(all_paths))
    if selected_path is None:
        return

    directory = os.path.expanduser(selected_path)
    command = "start alacritty.exe -e nvim ."

    is_cpp = "cmakelists.txt" in (i.lower() for i in os.listdir(directory))
    print("IS_CPP={}".format(is_cpp))
    if is_cpp:
        command = (
            r'call "c:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64 &&'
            + command
        )

    print(directory, command)
    subprocess.call(command, cwd=directory, shell=True)


if __name__ == "__main__":
    main()
