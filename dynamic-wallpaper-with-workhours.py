#!/usr/bin/python3

# inspired by https://github.com/adi1090x/dynamic-wallpaper

import os
import sys
import datetime
from pathlib import Path
import subprocess
import argparse
import shutil

PYWAL = shutil.which("wal")
if PYWAL is None:
    print(
        "This program requires installing `wal` (https://github.com/dylanaraps/pywal)",
        file=sys.stderr,
    )
    exit(1)

THIS_FILE = Path(__file__)
# THIS_DIR = THIS_FILE.parent

parser = argparse.ArgumentParser(
    description="This script is meant to be used in cron, where it will dynamically update wallpaper based on time of day. It will also use work wallpaper during working hours."
)
parser.add_argument("-r", "--root-path", required=True)
parser.add_argument("-w", "--wallpaper-name", required=True)
parser.add_argument("-t", "--theme-folder", required=True)
parser.add_argument(
    "-cron",
    "--show-cron-command",
    help="show cron command to use, then exit",
    action="store_true",
)
parser.add_argument(
    "-work",
    "--force-work-mode",
    help="force to use working theme",
    action="store_true",
)
parser.add_argument(
    "-s",
    "--set-mode-for-today",
    choices=["work", "normal", "clear"],
)

args = parser.parse_args()

ROOT_PATH = Path(args.root_path)

if args.show_cron_command:
    var_line = ""
    for var in [
        "DISPLAY",
        "DESKTOP_SESSION",
        "DBUS_SESSION_BUS_ADDRESS",
        "XDG_RUNTIME_DIR",
    ]:
        var_line += f'{var}="{os.environ.get(var, "")}" '
    print(
        f"""\
# Edit your crontab and add a job
$ crontab -e

# Add this line
0 * * * * env {var_line} {THIS_FILE} -r {args.root_path} -w {args.wallpaper_name} -t {args.theme_folder}
"""
    )
    exit()


now = datetime.datetime.now()

is_weekday = now.weekday() <= 4
is_working_hour = 8 <= now.hour <= 18

work_mode = is_weekday and is_working_hour

# try to see if user had set a preference for today
pref_fname = f"/tmp/{THIS_FILE.name}.{now.strftime('%Y-%m-%d')}"


if args.set_mode_for_today == "clear":
    try:
        os.remove(pref_fname)
    except FileNotFoundError:
        pass

elif args.set_mode_for_today:
    with open(pref_fname, "w") as f:
        f.write(args.set_mode_for_today)

try:
    with open(pref_fname, "r") as f:
        cur_mode = f.read()
    if cur_mode == "work":
        work_mode = True
    elif cur_mode == "normal":
        work_mode = False
except FileNotFoundError:
    # no today preference
    pass

if args.force_work_mode:
    work_mode = True


def get_file(path: Path, name: str):
    return next(path.glob(f"{name}.*"))


def set_wallpaper(filename: str):
    subprocess.check_output([PYWAL, "-i", filename])


if work_mode:
    set_wallpaper(get_file(ROOT_PATH, args.wallpaper_name))
else:
    set_wallpaper(get_file(ROOT_PATH / args.theme_folder, now.hour))
