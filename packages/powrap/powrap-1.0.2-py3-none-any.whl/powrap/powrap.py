"""Fix style of uncommitted po files, or all if --all is given."""

import argparse
import difflib
import os
import sys
from pathlib import Path
from subprocess import CalledProcessError, check_output, run
from tempfile import NamedTemporaryFile
from typing import Iterable, Tuple

from tqdm import tqdm

from powrap import __version__


class MsgcatNotFoundError(Exception):
    """Raised when the msgcat utility cannot be found."""


def _run_msgcat(po_content: str, output_file: str, no_wrap: bool) -> None:
    args = ["msgcat", "-", "-o", output_file]
    if no_wrap:
        args[1:1] = ["--no-wrap"]
    try:
        run(args, encoding="utf-8", check=True, input=po_content)
    except FileNotFoundError as err:
        raise MsgcatNotFoundError from err


def check_style(
    po_files: Iterable[str], no_wrap=False, quiet=False, diff=False
) -> Tuple[int, int]:
    """Check style of given po_files.

    Prints errors on stderr and returns the number of errors found.
    """
    would_rewrap = 0
    errors = 0
    for po_path in tqdm(po_files, desc="Checking wrapping of po files", disable=quiet):
        try:
            with open(po_path, encoding="UTF-8") as po_file:
                po_content = po_file.read()
        except OSError as open_error:
            tqdm.write(f"Error opening '{po_path}': {open_error}")
            errors += 1
            continue

        delete = os.name == "posix" and sys.platform != "cygwin"

        with NamedTemporaryFile("w+", delete=delete, encoding="utf-8") as tmpfile:
            try:
                _run_msgcat(po_content, tmpfile.name, no_wrap)
            except CalledProcessError as run_error:
                tqdm.write(f"Error processing '{po_path}': {run_error}")
                errors += 1
                continue
            new_po_content = tmpfile.read()
            if po_content != new_po_content:
                would_rewrap += 1
                print("Would rewrap:", po_path, file=sys.stderr)
                if diff:
                    for line in difflib.unified_diff(
                        po_content.splitlines(keepends=True),
                        new_po_content.splitlines(keepends=True),
                    ):
                        print(line, end="", file=sys.stderr)
        if not delete:
            os.remove(tmpfile.name)
    return would_rewrap, errors


def fix_style(po_files, no_wrap=False, quiet=False) -> int:
    """Fix style of given po_files."""
    errors = 0
    for po_path in tqdm(po_files, desc="Fixing wrapping of po files", disable=quiet):
        try:
            with open(po_path, encoding="UTF-8") as po_file:
                po_content = po_file.read()
        except OSError as open_error:
            tqdm.write(f"Error opening '{po_path}': {open_error}")
            errors += 1
            continue
        _run_msgcat(po_content, po_path, no_wrap)
    return errors


def parse_args():
    """Parse powrap command line arguments."""

    def path(path_str):
        path_obj = Path(path_str)
        if not path_obj.exists():
            raise argparse.ArgumentTypeError(f"File {path_str!r} does not exists.")
        if not path_obj.is_file():
            raise argparse.ArgumentTypeError(f"{path_str!r} is not a file.")
        try:
            path_obj.read_text(encoding="utf-8")
        except PermissionError as read_error:
            raise argparse.ArgumentTypeError(
                "{path_str!r}: Permission denied."
            ) from read_error
        return path_obj

    parser = argparse.ArgumentParser(
        prog="powrap",
        description="Ensure po files are using the standard gettext format",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""exit code:
    0:nothing to do
    1:would rewrap
    2:some files could not be formatted
  127:msgcat not found""",
    )
    parser.add_argument(
        "-m",
        "--modified",
        action="store_true",
        help="Use git to find modified files instead of passing them as arguments.",
    )
    parser.add_argument(
        "-C",
        help="To use with --modified to tell where the git "
        "repo is, in case it's not in the current working directory.",
        type=Path,
        dest="git_root",
        default=Path.cwd(),
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Do not show progress bar."
    )
    parser.add_argument(
        "-d",
        "--diff",
        action="store_true",
        help="Don't write the files back, just output a diff for each file on stdout "
        "(implies --check).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Don't write the files back, just return the status. "
        "See --help for how to interpret return codes. ",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument(
        "--no-wrap",
        action="store_true",
        help="see `man msgcat`, useful to sed right after.",
    )
    parser.add_argument("po_files", nargs="*", help="po files.", type=path)
    args = parser.parse_args()
    if not args.po_files and not args.modified:
        parser.print_help()
        sys.exit(1)
    if args.po_files and args.modified:
        parser.print_help()
        sys.exit(1)
    return args


def do_main():
    """Powrap main function (parsing command line and all)."""
    args = parse_args()
    if args.git_root:
        os.chdir(args.git_root)
    if args.modified:
        git_status = check_output(
            ["git", "status", "--porcelain", "--no-renames"],
            encoding="utf-8",
        )
        git_status_lines = [
            line.split(maxsplit=2) for line in git_status.split("\n") if line
        ]
        args.po_files.extend(
            Path(filename)
            for status, filename in git_status_lines
            if filename.endswith(".po") and status != "D"
        )
    if not args.po_files:
        print("Nothing to do, exiting.")
        sys.exit(0)
    if args.check or args.diff:
        would_rewrap, errors = check_style(
            args.po_files, args.no_wrap, args.quiet, args.diff
        )
    else:
        would_rewrap = 0
        errors = fix_style(args.po_files, args.no_wrap, args.quiet)
    ecode = 2 if errors else 1 if would_rewrap else 0
    sys.exit(ecode)


def main():
    """Powrap main entrypoint."""
    try:
        do_main()
    except MsgcatNotFoundError:
        print("msgcat utility not found, cannot continue", file=sys.stderr)
        sys.exit(127)
