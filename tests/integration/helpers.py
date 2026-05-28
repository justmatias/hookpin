from pathlib import Path

from hookpin.cli import main


def run_hookpin(*configs: Path | str, lockfile: Path, extra: list[str] | None = None) -> int:
    argv: list[str] = []
    for config in configs:
        argv += ["--config", str(config)]
    argv += ["--lockfile", str(lockfile)]
    if extra:
        argv += extra
    return main(argv)
