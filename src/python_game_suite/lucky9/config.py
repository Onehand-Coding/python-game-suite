from pathlib import Path
from typing import List


def get_current_dir() -> Path:
    current_dir = Path(__file__).parent
    while not (current_dir / "pyproject.toml").exists():
        if current_dir == current_dir.parent:
            raise FileNotFoundError("Could not find project root containing 'pyproject.toml'.")
        current_dir = current_dir.parent

    return current_dir


def create_dirs(paths: List[Path]) -> None:
    for path in paths:
        path.mkdir(exist_ok=True)


ROOT_DIR = get_current_dir()

ASSETS_DIR = ROOT_DIR / "src" / "python_game_suite" / "lucky9" / "assets"
DATA_DIR = ROOT_DIR / "src" / "python_game_suite" / "lucky9" / "data"
SOUND_ASSETS_DIR = ASSETS_DIR / "sounds"
IMAGE_ASSETS_DIR = ASSETS_DIR / "images"

Lucky9_game_dirs: List = [ASSETS_DIR,DATA_DIR, SOUND_ASSETS_DIR, IMAGE_ASSETS_DIR]

create_dirs(Lucky9_game_dirs)
