import os
import subprocess
import sys
from glob import glob
from pathlib import Path

from iterfzf import iterfzf
from win32 import win32api, win32gui, win32process

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

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
    command = 'wezterm.exe start --always-new-process --cwd "{}" -- '.format(directory)

    cmd = "nvim"
    is_godot = (Path(directory) / "project.godot").exists()
    if is_godot:
        cmd += " --listen 127.0.0.1:9696"
    cmd += " ."

    is_cpp = False
    for filename in ("cmakelists.txt", "makefile"):
        is_cpp |= filename in (i.lower() for i in os.listdir(directory))
    print("IS_CPP={}".format(is_cpp))
    if is_cpp or is_godot:
        d = os.path.join(directory, ".globalignore")
        if not os.path.exists(d):
            os.mkdir(d)

        script_file_path = os.path.join(d, ".wezterm.temp.bat")
        with open(script_file_path, "w") as out_file:
            out_file.write(
                rf"""
call "c:\Users\user\dev\home\emsdk\emsdk.bat" activate latest
call "c:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
set EMSCRIPTEN=c:\Users\user\dev\home\emsdk\upstream\emscripten
{cmd}"""
            )

        cmd = 'cmd /C "{}"'.format(script_file_path)

    command += cmd

    def callback(hwnd, pid):
        if win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
            win32gui.ShowWindow(hwnd, 0)

    win32gui.EnumWindows(callback, os.getppid())

    Path(r"c:\Users\user\Downloads\1.txt").write_text(command)

    print(directory, command)

    directory_formatted = str(Path(directory).relative_to(Path(directory).parent))

    subprocess.Popen(
        command,
        shell=False,
        start_new_session=False,
        creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        close_fds=True,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
