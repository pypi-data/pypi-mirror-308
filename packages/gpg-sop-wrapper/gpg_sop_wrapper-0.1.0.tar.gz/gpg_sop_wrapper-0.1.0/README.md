<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# gpg-sop-wrapper - wrap a SOP implementation, simulate a GnuPG interface

\[[Home][ringlet-home] | [Download][ringlet-download] | [GitLab][gitlab] | [ReadTheDocs][readthedocs]\]

## Overview

The `gpg-sop-wrapper` tool was created for the specific purpose of using
`debsign` to sign a Debian package's changes file, but with a SOP tool
(e.g. Sequoia's `sqop` implementation) instead of GnuPG.
As such, it only supports a very limited number of GnuPG's options - basically
the ones that `debsign` uses to invoke `gpg` - and translates `--clearsign` to
an `sqop inline-sign` invocation.

The `gpg-sop-wrapper` tool will invoke a program named `sop` by default;
this may be overridden using the `WRAPPED_SOP` environment variable.

## Examples

Sign a Debian source package's changes file using `sqop` instead of `gpg`:

``` sh
env WRAPPED_SOP=sqop debsign -k /path/to/secret/keyfile -p gpg-sop-wrapper pkgver_source.changes
```

## Contact

The `gpg-sop-wrapper` library was written by [Peter Pentchev][roam].
It is developed in [a GitLab repository][gitlab].
This documentation is hosted at [Ringlet][ringlet-home] with a copy at [ReadTheDocs][readthedocs].

[roam]: mailto:roam@ringlet.net "Peter Pentchev"
[gitlab]: https://gitlab.com/ppentchev/gpg-sop-wrapper "The gpg-sop-wrapper GitLab repository"
[readthedocs]: https://gpg-sop-wrapper.readthedocs.io/ "The gpg-sop-wrapper ReadTheDocs page"
[ringlet-home]: https://devel.ringlet.net/misc/gpg-sop-wrapper/ "The Ringlet gpg-sop-wrapper homepage"
[ringlet-download]: https://devel.ringlet.net/misc/gpg-sop-wrapper/download/ "The Ringlet gpg-sop-wrapper download page"
