import shutil
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
SHARED_FIXTURES = Path(__file__).parent.parent / "fixtures"


def config(tmp_path: Path, fixtures_dir: Path, name: str) -> Path:
    dest = tmp_path / "config.yaml"
    shutil.copy(fixtures_dir / name, dest)
    return dest


def shared_config(tmp_path: Path, name: str) -> Path:
    return config(tmp_path, SHARED_FIXTURES, name)


def local_config(tmp_path: Path, name: str) -> Path:
    return config(tmp_path, FIXTURES, name)
