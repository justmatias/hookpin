import re

from ruamel.yaml import YAML

# Matches: name[extras]==version  (extras and pre-release version segments optional)
PIN_RE = re.compile(r"^([A-Za-z0-9_.-]+)(\[[^\]]+\])?==([\d.]+(?:[a-z0-9.+-]*)?)$")

NORMALIZE_RE = re.compile(r"[-_.]+")

YAML_INSTANCE = YAML()
YAML_INSTANCE.preserve_quotes = True
YAML_INSTANCE.indent(mapping=2, sequence=4, offset=2)
