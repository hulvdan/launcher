import sys
import os
import subprocess
from glob import glob
from iterfzf import iterfzf

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

HOME_PATH = os.path.expanduser(os.path.normpath("~/"))

PATHS = [
    "~/Downloads/",
    "~/dev/",
    "~/dev/*/",
    "~/dev/gdev/*/",
    "~/dev/home/*/",
    "~/dev/home2/*/",
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
    command = r"""
        call c:\Users\user\dev\home2\emsdk\emsdk.bat activate latest
        set EMSCRIPTEN=c:\Users\user\dev\home2\emsdk\upstream\emscripten
        code {}
    """.format(directory)

    with open('_.bat', 'w', encoding='utf-8') as out_file:
        out_file.write(command)
    subprocess.Popen(
        '_.bat',
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
