"""Organizes files in a directory by their extension."""

# Robert Olson
# pylint: disable=line-too-long

import datetime
import os
import re
import shelve
import shutil
import statistics
import sys
from pathlib import Path
from typing import Callable, Optional

import appdirs
import rich
import rich.traceback
import survey
import toml
import typer
from click import option
from typer import Argument, Option

PathOrNone = Optional[Path]

main_app = typer.Typer()

archive_app = typer.Typer()
config_app = typer.Typer()
edit_app = typer.Typer()
# log_app = typer.Typer()


main_app.add_typer(archive_app, name="archive", help="Clean an existing archive.")
main_app.add_typer(config_app, name="config", help="Edit config file.")
# main_app.add_typer(log_app, name="log", help="View and edit log file.")
config_app.add_typer(edit_app, name="edit", help="Edit archive parameters.")


_THIS_FILE = Path(__file__)

_PROMPT = f"rob.{Path(__file__).stem}> "
_PROMPT_STYLE = "[white on blue]"
_ERROR_STYLE = "[red on black]"

_USER_CONFIG_FILE = Path(appdirs.user_config_dir()) / "robolson" / "clean" / "config" / "clean.toml"
_UNDO_FILE = Path(appdirs.user_data_dir()) / "robolson" / "clean" / "data" / "undo.db"
_LOG_FILE = Path(appdirs.user_data_dir()) / "robolson" / "clean" / "data" / "system_calls.log"
_LOG_FILE.touch()

_BLACKLIST_FILE = Path(appdirs.user_data_dir()) / "robolson" / "clean" / "data" / "ignore.db"

if not _UNDO_FILE.exists():
    os.makedirs(_UNDO_FILE.parent, exist_ok=True)
    db = shelve.open(str(_UNDO_FILE))
    db.close()

_BASE_CONFIG_FILE = _THIS_FILE.parent / "config" / "clean.toml"
with open(_BASE_CONFIG_FILE, "r") as fp:
    _SETTINGS = toml.load(fp)

if _USER_CONFIG_FILE.exists():
    with open(_USER_CONFIG_FILE, "r") as fp:
        USER_SETTINGS = toml.load(fp)
        _SETTINGS.update(USER_SETTINGS)

else:
    _USER_CONFIG_FILE.parent.mkdir(parents=True)
    _USER_CONFIG_FILE.touch(exist_ok=True)
    with open(_USER_CONFIG_FILE, "w") as fp:
        toml.dump(_SETTINGS, fp)


# _CROWDED_FOLDER = _SETTINGS["CROWDED_FOLDER"]  # number of files that is 'crowded'
_FILE_TYPES: dict[str, list[str]] = _SETTINGS[
    "FILE_TYPES"
]  # dictionary of (folder, file-types) pairs
ARCHIVE_FOLDERS = list(_FILE_TYPES.keys())
_EXCLUSIONS = _SETTINGS["EXCLUSIONS"]  # list of files to totally ignore
MONTHS = _SETTINGS["MONTHS"]  # strings to use when writing names of months
MONTHS.insert(0, None)

# _COMMANDS = []


def generate_extension_handler(file_types: dict[str, list[str]]) -> dict[str, str]:
    """Returns a dictionary that associates extension keys with their assigned file type / folder name."""
    extension_handler: dict[str, str] = {}
    for file_type in file_types.keys():
        for extension in file_types[file_type]:
            extension_handler[extension] = file_type

    return extension_handler


_EXTENSION_HANDLER = generate_extension_handler(_FILE_TYPES)


def isolate_crowded_folders(folders: list[Path], crowded_threshold: int = 20) -> list[Path]:
    """Return a list of directories with many files inside.
    post: True"""

    crowded = []

    for folder in folders:
        if folder.is_file():
            continue

        if len(list(folder.glob("*.*"))) > crowded_threshold:
            crowded.append(folder)

    return crowded


def approve_list(
    target: list, desc: str = "", repr_func=None, maximum: Optional[int] = None
) -> list:
    """Returns a user-approved subset of target list."""

    if not target:
        return []

    approved_targets = []

    approved_targets = survey.routines.basket(desc, options=target)
    if approved_targets:
        approved_list = [v for i, v in enumerate(target) if i in approved_targets]
    else:
        approved_list = []

    return approved_list

    # final_choice = False
    # invalid = False
    # while not final_choice:
    #     rich.print(desc, end="\n\n")
    #     for count, item in enumerate(target):
    #         if repr_func:
    #             display = repr_func(item)
    #         else:
    #             display = item

    #         style = "[green]" if item in approved_targets else "[red]"

    #         rich.print(f" {style}{count+1}.) {display}")

    #     style = _PROMPT_STYLE if not invalid else _ERROR_STYLE
    #     rich.print(
    #         f"\n{style}Toggle items by entering their associated list index, enter 'a' to toggle ALL items, or press Enter to continue."
    #     )
    #     choice = input(f"{_PROMPT}")
    #     invalid = False
    #     try:
    #         if not choice:
    #             final_choice = True

    #         if choice in ["a", "A", "all", "ALL"]:
    #             count = 1
    #             while count <= len(target):
    #                 if target[count - 1] in approved_targets:
    #                     approved_targets.remove(target[count - 1])
    #                 else:
    #                     approved_targets.insert(count - 1, target[count - 1])
    #                 if maximum and len(approved_targets) > maximum:
    #                     approved_targets = approved_targets[
    #                         len(approved_targets) - maximum :
    #                     ]
    #                 count += 1

    #             continue

    #         choice = int(choice)
    #         if 1 <= choice <= len(target):
    #             if target[choice - 1] in approved_targets:
    #                 approved_targets.remove(target[choice - 1])
    #             else:
    #                 # approved_targets.insert(choice - 1, target[choice - 1])
    #                 approved_targets.append(target[choice - 1])
    #             if maximum and len(approved_targets) > maximum:
    #                 approved_targets = approved_targets[
    #                     len(approved_targets) - maximum :
    #                 ]
    #         else:
    #             invalid = True

    #     except (SyntaxError, ValueError):
    #         invalid = True

    # return approved_targets


def approve_dict(
    target: dict,
    desc: str = "",
    repr_func: Callable[..., str] | None = None,
    maximum: int | None = None,
) -> dict:
    """Returns a user-approved subset of target dictionary."""

    if not target:
        return {}

    if not repr_func:
        source_width = max([len(str(key)) for key in target.keys()])
        dest_width = max(len(str(target[key])) for key in target.keys())

        def default_format(key):
            return f"{str(key):<{source_width}} -> {str(target[key]):>{dest_width}}"

        repr_func = default_format

    list_of_keys = list(target.keys())

    formatted_keys = [repr_func(key) for key in list_of_keys]
    approved_targets = survey.routines.basket(desc, options=formatted_keys)
    approved_keys = [key for i, key in enumerate(list_of_keys) if i in approved_targets]

    approved_dict = {key: target[key] for key in approved_keys}

    return approved_dict

    # approved_keys = []
    # frozen_keys = list(target.keys())
    # final_choice = False
    # invalid = False
    # while not final_choice:
    #     rich.print(desc, end="\n\n")
    #     for count, key in enumerate(frozen_keys):
    #         if key in approved_keys:
    #             # rich.print(f" [green]{count+1:2}.) {key}[yellow]->[green]{target[key]}")
    #             rich.print(f" [green]{count+1:2}.){repr_func(key)}")
    #         else:
    #             # rich.print(f" [red]{count+1}.) {key}[yellow]->[red]{target[key]}")
    #             rich.print(f" [red]{count+1:2}.){repr_func(key)}")

    #     style = _PROMPT_STYLE if not invalid else _ERROR_STYLE
    #     rich.print(
    #         f"\n{style}Toggle items by entering their associated list index, or enter 'a' to toggle ALL or press Enter to continue."
    #     )
    #     choice = input(f"{_PROMPT}")
    #     invalid = False
    #     try:
    #         if not choice:
    #             final_choice = True

    #         if choice in ["a", "A", "all", "ALL"]:
    #             count = 1
    #             while count <= len(target):
    #                 if frozen_keys[count - 1] in approved_keys:
    #                     approved_keys.remove(frozen_keys[count - 1])
    #                 else:
    #                     approved_keys.insert(count - 1, frozen_keys[count - 1])

    #                 count += 1

    #             if maximum and len(approved_keys) > maximum:
    #                 approved_keys = approved_keys[len(approved_keys) - maximum :]

    #             continue

    #         choice = int(choice)
    #         if 1 <= choice <= len(target):
    #             if frozen_keys[choice - 1] in approved_keys:
    #                 approved_keys.remove(frozen_keys[choice - 1])
    #             else:
    #                 # approved_keys.insert(choice - 1, frozen_keys[choice - 1])
    #                 approved_keys.append(frozen_keys[choice - 1])
    #             if maximum and len(approved_keys) > maximum:
    #                 approved_keys = approved_keys[len(approved_keys) - maximum :]
    #         else:
    #             invalid = True

    #     except (SyntaxError, ValueError):
    #         invalid = True

    # return {key: target[key] for key in approved_keys}


def uncrowd_folder(folder: Path, yes_all: bool = False) -> dict[Path, Path]:
    """Return a dictionary that associates crowded files in a folder with a better Path."""

    files = folder.glob("*.*")
    file_targets: dict[Path, Path] = {}
    for file in files:
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file.absolute()))

        f_month = MONTHS[last_modified.month]
        f_year = last_modified.year

        target_folder = (
            Path(f"{file.parent}")
            / f"{file.parent.parent.name} {last_modified.month} ({f_month}) {f_year}"
        )

        file_targets[file] = target_folder / file.name

    if yes_all:
        return file_targets
    else:
        return approve_dict(file_targets, f"Select files in '{folder.absolute()}' to uncrowd:")


def associate_files(
    files: list[Path],
    root: Path = Path("."),
    extension_handler: dict[str, str] | None = None,
    default_folder: Path = Path("misc"),
    yes_all: bool = True,
) -> dict[Path, Path]:
    """Returns a dictionary that associates passed files with their most organized location."""

    if not extension_handler:
        extension_handler = {}

    os.chdir(root.absolute())

    file_targets: dict[Path, Path] = {}

    uncrowded_pattern = re.compile(r"\w+ \d\d? \(\w+\) \d\d\d\d")

    for file in files:
        # ignore registered archive folders
        if file.name in _FILE_TYPES.keys() or file.name == "misc":
            continue

        # ignore folders if no user interaction
        if not file.suffix and yes_all:
            continue

        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        file_type_folder = extension_handler.get(file.suffix, default_folder.name)

        # if file_type_folder == "misc" and not yes_all:
        #     candidate = approve_list(
        #         target=list(_FILE_TYPES.keys()),
        #         desc=f"Move '{file.absolute()}' to which folder?\n(Or leave selection empty to skip.)",
        #         maximum=1,
        #     )

        #     if not candidate:
        #         continue

        #     file_type_folder = candidate[0]

        f_year: str = str(last_modified.year)
        f_month: str = str(last_modified.month)
        target_folder = Path(f"{file_type_folder}") / f"{file_type_folder} {f_year}"

        sub_folders = [folder for folder in target_folder.glob("*") if folder.is_dir()]

        # if target folder has sub-folders from previous uncrowding, follow the uncrowded naming protocol
        if any(uncrowded_pattern.match(folder.name) for folder in sub_folders):
            target_folder = (
                target_folder / f"{file_type_folder} {last_modified.month} ({f_month}) {f_year}"
            )

        file_targets[file] = target_folder / file.name

    return file_targets


# def handle_files(
#     files: list[str],
#     folder: str = "misc",
#     month: bool = False,
#     yes_all: bool = True,
# ) -> None:
#     """Organizes files by last modified date."""
#     choice = ""

#     for file in files:
#         last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file))
#         f_month = MONTHS[last_modified.month]

#         file_size = os.stat(file).st_size

#         f_year = last_modified.year
#         if file_size > 150_000_000:
#             target_folder = os.path.join("Large_Files", str(f_year))
#         else:
#             target_folder = os.path.join(folder, f"{folder} {str(f_year)}")

#         if month:
#             target_folder = os.path.join(
#                 target_folder, f"{folder} {last_modified.month} ({f_month}) {f_year}"
#             )
#         os.makedirs(target_folder, exist_ok=True)

#         while choice not in ["y", "yes", "n", "no", "a", "all", "d", "del"]:
#             rich.print(
#                 f"[yellow]mv '{file}' '{target_folder}\\{os.path.split(file)[1]}'\n[green](y)es[white] / [red](n)o[white] / [green]yes_to_(a)ll[white] / [red](d)el?"
#             )
#             choice = input(f"{_PROMPT}") if not yes_all else "y"

#         match choice:
#             case "y" | "yes":
#                 _COMMANDS.append(("mv", Path(file), Path(target_folder) / Path(file)))

#             case "a" | "all":
#                 _COMMANDS.append(("mv", Path(file), Path(target_folder) / Path(file)))
#                 yes_all = True

#             case "d" | "del":
#                 os.makedirs("delete_me", exist_ok=True)
#                 _COMMANDS.append(("mv", Path(file), Path("delete_me") / Path(file)))


#  ^^^^^^^^^^^^^^^^^^^^^^^^^^
#  </ def handle_files()>
#  ^^^^^^^^^^^^^^^^^^^^^^^^^^


def remove_empty_dir(path: str | Path):
    """Remove empty folder."""

    try:
        os.rmdir(path)
        print(f"Removing empty folder ({path}).")
    except OSError:
        pass


@archive_app.command(name="empty")
def remove_empty_dirs(target: Path = Path(".")):
    """Recursively remove empty folders."""

    for trunk, dirnames, _ in os.walk(target, topdown=False):
        for dirname in dirnames:
            remove_empty_dir(os.path.realpath(os.path.join(trunk, dirname)))

    remove_empty_dir(target)


@main_app.command()
def log() -> None:
    """Load the log file which contains a record of all executed system commands."""
    os.startfile(_LOG_FILE)


@main_app.command()
def undo(
    target: Path = Argument(Path("."), help="Target folder to undo operations."),
    yes_all: bool = Option(False, help="Automatically confirm all actions.", show_default=False),
    dry_run: bool = Option(False, help="Print commands without executing.", show_default=False),
) -> None:
    """Undo file manipulations in target directory."""

    undo_commands = {}
    with shelve.open(str(_UNDO_FILE)) as db:
        try:
            old_commands = db[str(target.absolute()).lower()]
            for source, dest in old_commands.items():
                undo_commands[dest] = target.absolute() / source
                # undo_commands.append((command, dest, source))
                # _COMMANDS.append((command, dest, source))

        except KeyError:
            rich.print(f"[red]No recorded commands executed on ({Path(target).absolute()}).")
            exit(1)

    preview_mvs(undo_commands, absolute=True)

    if dry_run:
        return

    if yes_all:
        choice = "y"
    else:
        rich.print("[red]Are you sure? (y/n)")
        choice = input(f"{_PROMPT}")

    if choice in ["y", "yes", "Y", "YES"]:
        try:
            execute_move_commands(undo_commands)

        except Exception as e:
            with shelve.open(str(_UNDO_FILE)) as db:
                del db[str(target.absolute()).lower()]
            print(e)
            exit(1)
        with shelve.open(str(_UNDO_FILE)) as db:
            db[str(target.absolute()).lower()] = undo_commands

            # pickle.dump(_COMMANDS, _UNDO_FILE)

    remove_empty_dirs(target)


#  ^^^^^^^^^^^^^^^^^^^^^^^^^^
#  </ def undo()>
#  ^^^^^^^^^^^^^^^^^^^^^^^^^^


def preview_mvs(renames: dict[Path, Path], absolute: bool = False) -> Callable:
    """Print a list of mv targets.
    post: True"""
    for source, dest in renames.items():
        rich.print(
            f"mv [green]{source.absolute() if absolute else source.name} [red]{dest.absolute()}"
        )


def execute_move_commands(commands: dict[Path, Path], target: Path = Path("."), yes_all=False):
    """Execute a sequence of file move commands.

    Args:
                                                                                                                                    commands: A dictionary with source keys and destination values.
    post: True
    """
    sources = list(commands.keys())
    for source in sources:
        if not source.suffix:  # if source is a folder, rather than a file
            if yes_all:  # ignore folders if no user interaction
                continue
            # candidate = approve_list(
            #     target=list(_FILE_TYPES.keys()),
            #     desc=f"Move '{source.absolute()}' to which folder?\n(Or leave selection empty to skip.)",
            #     maximum=1,
            # )

            # if not candidate:
            #     continue

            # file_type_folder = Path(candidate[0])

            candidate = survey.routines.select(
                f"Move '{source.absolute()}' to which folder?",
                options=ARCHIVE_FOLDERS,
            )

            file_type_folder = Path(ARCHIVE_FOLDERS[candidate])

            target_folder = associate_files(
                files=[source],
                extension_handler={"": str(file_type_folder)},
                default_folder=file_type_folder,
            )
            os.makedirs(target_folder[source].parent.absolute(), exist_ok=True)
            shutil.move(source.absolute(), target_folder[source].absolute())
            # today = datetime.datetime.today().isoformat(timespec="minutes")
            today = datetime.datetime.today().ctime()

            with open(_LOG_FILE, "a", encoding="utf-8") as fp:
                fp.write(f"{today}\nmv {source.absolute()} {target_folder[source].absolute()}\n")
            continue
        try:
            breakpoint()
            os.makedirs(commands[source].parent.absolute(), exist_ok=True)
            shutil.move(source.absolute(), commands[source].absolute())
            today = datetime.datetime.today().ctime()

            with open(_LOG_FILE, "a", encoding="utf-8") as fp:
                fp.write(f"{today}\nmv {source.absolute()} {commands[source].absolute()}\n")

        # File of Same Name Has Already Been Moved To Folderg
        except shutil.Error as e:
            print(e)
        except FileNotFoundError:
            rich.print(f"{_ERROR_STYLE}{source.absolute()} not found.")
    with shelve.open(str(_UNDO_FILE)) as db:
        db[str(target.absolute()).lower()] = commands


def create_config():
    """Create a config file in users app data directory that overrides base settings.
    post: True"""

    os.makedirs(_USER_CONFIG_FILE.parent, exist_ok=True)
    shutil.copyfile(_BASE_CONFIG_FILE, _USER_CONFIG_FILE)
    print(f"User config file created at:\n{_USER_CONFIG_FILE}")


def gather_files(
    target: str | Path = Path("."),
    extensions: list[str] | None = None,
    recurse: bool = False,
    recursion_limit: int | None = None,
    exclusions: list[str] | None = None,
) -> list[Path]:
    """Return a list of files in target directory, optionally filtered by file extension(s) and exclusions."""
    glob_query: str = ""

    match (recurse, recursion_limit):
        case (True, None):
            glob_query = "**/." if recurse else "*."
        case (True, x) if x > 0:
            glob_query = "*/" * x + "*."
        case _:
            glob_query = "*."

    if extensions:
        glob_query += "".join({f"[{extension}]" for extension in extensions})
    else:
        glob_query += "*"

    all_files = Path(target).glob(glob_query)

    if all_files and exclusions:
        all_files = [Path(file) for file in all_files if file.name not in exclusions]

    if all_files:
        return list(all_files)

    return []


@main_app.command(name="files")
def clean_files(
    target: Path = Option(Path("."), help="Target folder to organize files."),
    recurse: bool = False,
    yes_all: bool = False,
    # extension_handler: dict[str, str] | None = None,
    exclusions: PathOrNone = None,
) -> None:
    """Clean the files by extension in target root directory."""
    extension_handler = _EXTENSION_HANDLER
    if recurse:
        root_files = target.rglob("*.*")
    else:
        # root_files = target.glob("*.*")
        root_files = target.glob("*")

    # breakpoint()

    if exclusions:
        root_files = [file for file in root_files if str(file.name) not in exclusions]

    target_mvs: dict[Path, Path] = associate_files(
        files=list(root_files), extension_handler=extension_handler, yes_all=yes_all
    )

    if yes_all:
        approved_mvs = target_mvs
    else:
        approved_mvs = approve_dict(
            target_mvs,
            f"Targeting '{target.absolute()}' for clean up.\n\nSelect files to archive:",
        )

    if approved_mvs:
        preview_mvs(approved_mvs)
        execute_move_commands(approved_mvs, target=target, yes_all=yes_all)


@archive_app.command(name="large")
def identify_large_files(
    target: Path = Argument(Path("."), help="Target folder to locate overly large files."),
    yes_all: bool = Option(False, help="Automatically confirm all actions."),
) -> None:
    """Find large files in target directory and offer to centralize them."""

    archive_folders = [Path(target) / f"{archive_folder}" for archive_folder in _FILE_TYPES.keys()]
    sub_folders = []
    all_files = []

    for folder in archive_folders:
        sub_folders.extend(list(folder.glob(f"{folder.name} [0-9][0-9][0-9][0-9]/")))

    for sub_folder in sub_folders:
        all_files.extend(sub_folder.rglob("*.*"))

    # all_files = gather_files(target=target, recurse=True, recursion_limit=3)
    if not all_files:
        rich.print("No archives found.")
        return

    file_sizes = [os.stat(file.absolute()).st_size for file in all_files]
    avg_file_size = sum(file_sizes) / len(file_sizes)
    if len(file_sizes) > 1:
        standard_deviation = statistics.stdev(file_sizes)
    else:
        standard_deviation = 0

    if yes_all:
        choice = "y"
    else:
        rich.print(
            f"Archived files average:\n\n{float(avg_file_size/1_000_000):_.2f} Mbs +/- {float(standard_deviation/1_000_000):_.2} Mbs\n\n{_PROMPT_STYLE}Isolate large files (default: >150 Mbs)? Y/N?\n(Enter an integer to specify large file treshold.)",
        )
        choice = input(f"{_PROMPT}")

    large: int = 0

    match choice:
        case ("y" | "Y" | "yes"):
            large = 150_000_000
        case ("n" | "N" | "no"):
            large = 150_000_000_000_000_000
        case x if re.match(r"\d+mbs?", x, re.IGNORECASE):
            large = int(re.match(r"([\d_]+) ?mbs?", x, re.IGNORECASE).group(1))
            large = large * 1_000_000
        case x if re.match(r"\d+kbs?", x, re.IGNORECASE):
            large = int(re.match(r"([\d_]+) ?kbs?", x, re.IGNORECASE).group(1))
            large = large * 1000
        case x if re.match(r"\d+$", x):
            large = int(x) * 1_000_000
        case _:
            large = 150_000_000_000_000_000

    large_files = [file for file in all_files if os.stat(file.absolute()).st_size > large]

    if yes_all:
        approved_files = large_files
    else:

        def show_file_size(x):
            return f"{x} ({float(os.stat(x.absolute()).st_size / 1000000):_.2f} Mb)"

        approved_files = approve_list(
            large_files,
            f"{_PROMPT_STYLE}Select large files to isolate:",
            repr_func=show_file_size,
        )
    if approved_files:
        large_mvs = associate_files(
            approved_files, default_folder=Path("large_files"), yes_all=yes_all
        )

        execute_move_commands(large_mvs)


@archive_app.command(name="crowded")
def identify_crowded_archives(
    target: Path = typer.Option(default=Path("."), help="target path"),
    threshold: int = typer.Option(default=20, help="number of files to qualify as crowded"),
    yes_all: bool = typer.Option(
        default=False, help="always apply all routines to all valid files"
    ),
) -> None:
    """Archives with file count exceeding threshold is sub-divided by month folders."""

    archive_folders = [Path(f"{key}") for key in _FILE_TYPES.keys()]
    all_folders = []
    for folder in archive_folders:
        all_folders.extend(list(folder.glob(f"{folder} [0-9][0-9][0-9][0-9]/")))

    crowded_folders = isolate_crowded_folders(all_folders, crowded_threshold=threshold)

    uncrowded_mvs = {}

    if not crowded_folders:
        return

    if yes_all:
        approved_folders = crowded_folders
    else:
        approved_folders = approve_list(
            crowded_folders, f"Choose folders to uncrowd (>{threshold} files):"
        )
    for folder in approved_folders:
        if yes_all:
            approved_mvs = uncrowd_folder(folder, yes_all=True)
        else:
            suggested_mvs = uncrowd_folder(folder)
            approved_mvs = approve_dict(
                suggested_mvs, "Are you sure you approve all these file movements?"
            )

        uncrowded_mvs.update(approved_mvs)
    if not yes_all:
        preview_mvs(uncrowded_mvs)
        execute_move_commands(uncrowded_mvs)


@main_app.callback()
def main(target: Path = Path("."), recurse: bool = False, yes_all: bool = False):
    all(target=target, recurse=recurse, yes_all=yes_all)


@main_app.command()
def all(target: Path = Path("."), recurse: bool = False, yes_all: bool = False):
    """Apply all available cleaning routines."""
    clean_files(target=target, recurse=recurse, exclusions=_EXCLUSIONS, yes_all=yes_all)
    identify_large_files(target=target, yes_all=yes_all)
    identify_crowded_archives(target=target, threshold=_SETTINGS["CROWDED_FOLDER"], yes_all=yes_all)
    remove_empty_dirs(target=target)

    return


@config_app.callback(invoke_without_command=True)
def config(ctx: typer.Context):
    if not ctx.invoked_subcommand:
        print("INTERACT")
        config_interact()


@config_app.command(name="add")
def add_archive(new_archive: str) -> None:
    """Add a new archive type."""
    _SETTINGS["FILE_TYPES"][new_archive] = []
    fp = open(_USER_CONFIG_FILE, "w")
    toml.dump(_SETTINGS, fp)
    fp.close()


@config_app.command(name="remove")
def remove_archive(target_archive: str) -> None:
    """Remove an archive type from the list."""
    del _SETTINGS["FILE_TYPES"][target_archive]
    fp = open(_USER_CONFIG_FILE, "w")
    toml.dump(_SETTINGS, fp)
    fp.close()
    print(f"Removed {target_archive} from archive list.")


@config_app.command(name="list")
def list_archives() -> None:
    """List recognized archive categories."""
    archives = (file_type for file_type in _SETTINGS["FILE_TYPES"].keys())
    print(" * " + "\n * ".join(e for e in archives))


@config_app.command(name="interact")
def config_interact() -> None:
    options = ["add", "remove", "edit", "exit"]

    while True:
        print("Current Archives\n----------------")
        list_archives()
        choice = survey.routines.select(options=options)
        choice = options[choice]

        match choice:
            case "add":
                form = {
                    "name": survey.widgets.Input(),
                    "extension": survey.widgets.Input(),
                }
                data = survey.routines.form(form=form)
                add_archive(data["name"])

            case "remove":
                selection = survey.routines.select(options=ARCHIVE_FOLDERS)
                remove_archive(ARCHIVE_FOLDERS[selection])

            case "edit":
                selection = survey.routines.select(options=ARCHIVE_FOLDERS)
                edit_archive(ARCHIVE_FOLDERS[selection])

            case "exit":  #
                exit(0)


@edit_app.callback(invoke_without_command=True)
def edit_default(ctx: typer.Context):
    if ctx.invoked_subcommand:
        return

    selection = survey.routines.select(options=ARCHIVE_FOLDERS)
    edit_archive(ARCHIVE_FOLDERS[selection])


@config_app.command(name="edit")
def edit_archive(target_archive: str):
    extensions = _SETTINGS["FILE_TYPES"][target_archive]
    print(f"{target_archive} extensions:\n * " + "\n * ".join(extensions))
    options = ["add", "remove", "edit"]
    selection = survey.routines.select(options=options)
    selection = options[selection]
    match selection:
        case "add":
            new_extension = survey.routines.input(
                f"Enter new extension for {target_archive} archive.\n{_PROMPT}"
            )
            add_extension(target_archive=target_archive, new_extension=new_extension)

        case "remove":
            candidate = survey.routines.select(options=extensions)
            remove_extension(target_archive=target_archive, target_extension=extensions[candidate])

    extensions = {}
    extensions = _SETTINGS["FILE_TYPES"][target_archive]


@edit_app.command(name="add")
def add_extension(target_archive: str, new_extension: str):
    _SETTINGS["FILE_TYPES"][target_archive].append(new_extension)
    fp = open(_USER_CONFIG_FILE, "w")
    toml.dump(_SETTINGS, fp)
    fp.close()

    print(f"Added {new_extension} to {target_archive}.")


@edit_app.command(name="remove")
def remove_extension(target_archive: str, target_extension: str):
    _SETTINGS["FILE_TYPES"][target_archive].remove(target_extension)
    fp = open(_USER_CONFIG_FILE, "w")
    toml.dump(_SETTINGS, fp)
    fp.close()

    print(f"Removed {target_extension} from {target_archive}.")


@main_app.callback()
def main():
    """Organize files in a folder."""


if __name__ == "__main__":
    if len(sys.argv) == 1:
        all()
        exit(0)

    main_app()
    # main()
