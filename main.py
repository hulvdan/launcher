import os
import subprocess

from win32 import win32api
from win32 import win32process
from win32 import win32gui

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
    command = 'wezterm.exe start --cwd "{}" -- '.format(directory)

    cmd = "nvim ."

    is_cpp = "cmakelists.txt" in (i.lower() for i in os.listdir(directory))
    print("IS_CPP={}".format(is_cpp))
    if is_cpp:
        d = os.path.join(directory, ".globalignore")
        if not os.path.exists(d):
            os.mkdir(d)

        script_file_path = os.path.join(d, ".wezterm.temp.bat")
        with open(script_file_path, "w") as out_file:
            out_file.write(
                r"""
call "c:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
nvim ."""
            )

        cmd = 'cmd /C "{}"'.format(script_file_path)

    command += cmd

    def callback(hwnd, pid):
        if win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
            win32gui.ShowWindow(hwnd, 0)

    win32gui.EnumWindows(callback, os.getppid())

    print(directory, command)
    subprocess.Popen(
        command,
        shell=True,
        start_new_session=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


if __name__ == "__main__":
    main()
