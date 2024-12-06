# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Common definitions for the gpg-sop-wrapper library."""

from __future__ import annotations

import typing


if typing.TYPE_CHECKING:
    from typing import Final


VERSION: Final = "0.1.0"
"""The gpg-sop-wrapper library version, semver-like."""

DEFAULT_SOP_PROGRAM: Final = "sop"
"""The default name of the SOP tool to invoke."""
