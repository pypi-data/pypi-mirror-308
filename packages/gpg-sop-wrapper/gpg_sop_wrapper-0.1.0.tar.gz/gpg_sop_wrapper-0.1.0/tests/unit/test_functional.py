# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Make sure that `gpg-sop-wrapper run` starts up at least."""

from __future__ import annotations

import builtins
import functools
import os
import pathlib
import sys
import tempfile
import typing
from unittest import mock

import pytest

from gpg_sop_wrapper import __main__ as tmain
from gpg_sop_wrapper import defs


if typing.TYPE_CHECKING:
    from typing import Final


@functools.lru_cache
def utf8_env() -> dict[str, str]:
    """Prepare a UTF-8-capable environment for executing child processes."""
    env: Final = dict(os.environ)
    env["LC_ALL"] = "C.UTF-8"
    if "LANGUAGE" in env:
        del env["LANGUAGE"]
    return env


def test_version() -> None:
    """Make sure that `gpg-sop-wrapper --version` works."""
    lines: Final[list[str]] = []
    with (
        mock.patch.object(os, "environ", utf8_env()),
        mock.patch.object(sys, "argv", new=["whee", "--version"]),
        mock.patch.object(builtins, "print", new=lines.append),
        pytest.raises(SystemExit) as xerr,
    ):
        tmain.main()

    assert xerr.value.code == 0

    assert len(lines) == 1
    assert lines[0].startswith("gpg ")
    assert lines[0].split()[-1].startswith("2.")


@pytest.mark.parametrize(
    ("params", "expected"),
    [
        ([], "Exactly one of "),
        (["--version", "--clearsign"], "Exactly one of "),
        (["--clearsign", "--local-user", __file__, "--output", "/nonexistent"], "No keyfile "),
        (["--clearsign", "--local-user", __file__, __file__], "No keyfile "),
        (["--clearsign", "--output", "/nonexistent", __file__], "No keyfile "),
    ],
)
def test_bad_params(*, params: list[str], expected: str) -> None:
    """Invoke the program with bad command-line parameters, expect errors."""
    lines: Final[list[str]] = []
    with (
        mock.patch.object(os, "environ", utf8_env()),
        mock.patch.object(sys, "argv", new=["whee", *params]),
        mock.patch.object(builtins, "print", new=lines.append),
        pytest.raises(SystemExit) as xerr,
    ):
        tmain.main()

    code: Final = xerr.value.code
    assert isinstance(code, str)
    assert expected in code

    assert not lines


def test_run() -> None:
    """Invoke the program with good command-line parameters, expect the program to be executed."""
    with tempfile.TemporaryDirectory(prefix="gpg-sop-test.") as tempd_obj:
        tempd: Final = pathlib.Path(tempd_obj)
        sop: Final = tempd / defs.DEFAULT_SOP_PROGRAM
        sop.write_text(
            """#!/bin/sh

set -e

echo "Command-line arguments: ...$*..."
cat
""",
            encoding="UTF-8",
        )
        sop.chmod(0o755)

        env: Final = dict(utf8_env())
        env["PATH"] = f"{tempd}{os.path.pathsep}{env['PATH']}"

        keyfile: Final = tempd / "keyfile"
        keyfile.write_text("Hello\n", encoding="UTF-8")

        infile: Final = tempd / "infile"
        infile.write_text("Goodbye\n", encoding="UTF-8")

        outfile: Final = tempd / "outfile"

        with (
            mock.patch.object(os, "environ", env),
            mock.patch.object(
                sys,
                "argv",
                [
                    "whee",
                    "--clearsign",
                    "--local-user",
                    str(keyfile),
                    "--output",
                    str(outfile),
                    "--armor",
                    str(infile),
                ],
            ),
            pytest.raises(SystemExit) as xerr,
        ):
            tmain.main()

        assert xerr.value.code == 0

        lines: Final = outfile.read_text(encoding="UTF-8").splitlines()
        assert lines == [
            f"Command-line arguments: ...inline-sign --as clearsigned -- {keyfile}...",
            "Goodbye",
        ]
