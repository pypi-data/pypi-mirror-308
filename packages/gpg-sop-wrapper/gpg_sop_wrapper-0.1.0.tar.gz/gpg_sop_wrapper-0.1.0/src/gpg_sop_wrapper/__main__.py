# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Wrap a SOP implementation, simulate a GnuPG interface."""

from __future__ import annotations

import os
import pathlib
import subprocess  # noqa: S404
import sys
import typing

import click

from . import defs


if typing.TYPE_CHECKING:
    from typing import Final


@click.command(name="gpg-sop-wrapper")
@click.option("--armor", is_flag=True, expose_value=False, help="ignored")
@click.option("--clearsign", is_flag=True, help="Create an inline signature")
@click.option("--list-options", type=str, expose_value=False, help="ignored")
@click.option(
    "--local-user",
    type=click.Path(
        dir_okay=False,
        file_okay=True,
        exists=True,
        path_type=pathlib.Path,
        readable=True,
        resolve_path=True,
    ),
    help="Specify the path to the keyfile",
)
@click.option("--no-auto-check-trustdb", is_flag=True, expose_value=False, help="ignored")
@click.option(
    "--output",
    type=click.Path(dir_okay=False, file_okay=True, path_type=pathlib.Path, resolve_path=True),
    help="Specify the path to the signed file to create",
)
@click.option("--textmode", is_flag=True, expose_value=False, help="ignored")
@click.option("--version", is_flag=True, help="Display program version info and exit")
@click.argument(
    "infile",
    type=click.Path(
        dir_okay=False,
        file_okay=True,
        exists=True,
        readable=True,
        path_type=pathlib.Path,
        resolve_path=True,
    ),
    required=False,
)
def main(
    *,
    clearsign: bool,
    infile: pathlib.Path | None,
    local_user: pathlib.Path | None,
    output: pathlib.Path | None,
    version: bool,
) -> None:
    """Wrap a SOP implementation, simulate a GnuPG interface."""
    prog: Final = os.environ.get("WRAPPED_SOP", defs.DEFAULT_SOP_PROGRAM)

    if version:
        if clearsign:
            sys.exit("Exactly one of --version or --clearsign expected")

        print("gpg (GnuPG) 2.2.45")
        return

    if not clearsign:
        sys.exit("Exactly one of --version or --clearsign expected")

    if local_user is None or infile is None or output is None:
        sys.exit("No keyfile path (--local-user), input path, or output path (--output) specified")

    with infile.open(mode="rb") as f_in, output.open(mode="wb") as f_out:
        cmd: Final[list[pathlib.Path | str]] = [
            prog,
            "inline-sign",
            "--as",
            "clearsigned",
            "--",
            local_user,
        ]
        try:
            res: Final = subprocess.run(cmd, check=False, stdin=f_in, stdout=f_out)  # noqa: S603
        except (OSError, subprocess.CalledProcessError) as err:
            sys.exit(f"Could not execute `{prog}` to sign the data: {err}")
        if res.returncode != 0:
            sys.exit(f"The `{prog}` tool exited with code {res.returncode}")


if __name__ == "__main__":
    main()
