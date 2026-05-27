"""Shared regex patterns and YAML instance used across the package."""

import re

from ruamel.yaml import YAML  # pylint: disable=import-error

# Matches a PEP 508 dependency string: name[extras]<specifier>; marker
# Group 1: package name
# Group 2: optional [extras]
# Group 3: version specifier (stops before ; or whitespace)
# Group 4: optional PEP 508 environment marker (including the leading ; and any spaces)
SPECIFIER_RE = re.compile(
    r"^([A-Za-z0-9_.-]+)"
    r"(\[[^\]]+\])?"
    r"((?:~=|===?|!=|<=|>=|[<>])[^\s;]+)"
    r"(\s*;[^#\n]*)?"
    r"$"
)

# Matches individual specifier components inside a (possibly compound) specifier string
SPECIFIER_PART_RE = re.compile(r"(~=|===?|!=|<=|>=|[<>])([^\s,]+)")

NORMALIZATION_RE = re.compile(r"[-_.]+")

YAML_INSTANCE = YAML()
YAML_INSTANCE.preserve_quotes = True
YAML_INSTANCE.indent(mapping=2, sequence=4, offset=2)
