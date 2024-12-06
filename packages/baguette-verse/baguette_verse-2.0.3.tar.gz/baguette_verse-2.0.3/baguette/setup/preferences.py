"""
This module manages the BAGUETTE preferences folder (~/.baguette) and defines functions to read, write quand query these parameters.
"""

from pathlib import Path
from typing import Iterator
from hashlib import sha3_512

__all__ = ["preferences_dir", "global_preferences_dir", "install_seed", "get_gephi_path", "search_gephi_paths", "ask_user_for_gephi_path", "save_gephi_path"]





install_seed = sha3_512(f"{Path(__file__).absolute().parent.parent.resolve()}".encode()).digest().hex()
preferences_dir = Path(f"~/.baguette/{install_seed}").expanduser().resolve().absolute()
global_preferences_dir = preferences_dir.parent
global_preferences_dir.mkdir(exist_ok=True)
preferences_dir.mkdir(exist_ok=True)

def get_gephi_path() -> Path | None:
    """
    Returns the path to the Gephi executable.
    Returns None if it has not been set. Use default_gephi_paths to get a list of paths to try.
    """
    from pathlib import Path
    param_path = preferences_dir / "path_to_gephi.txt"
    if param_path.exists():
        if not param_path.is_file():
            raise FileExistsError(f"Path to parameter file for the Gephi executable exists and is not a file: '{param_path}'")
        return Path(param_path.read_text())

def search_gephi_paths() -> list[Path]:
    """
    Returns a list of paths to try for finding the Gephi executable.
    """
    from pathlib import Path
    from sys import platform
    from os import environ
    l : "list[Path]" = []

    if platform == "win32":
        for p in environ["PATH"].split(";"):
            p = Path(p)
            for name in ("gephi64.exe", "gephi.exe"):
                if p.parent.name.startswith("Gephi-") and (p / name).is_file():
                    l.append(p / name)
    
    return l

def ask_user_for_gephi_path() -> Path:
    """
    Asks the user for the path to Gephi and saves it under the preference file.
    """
    from pathlib import Path
    spath = input("Please provide the path to the Gephi executable as it could not be infered > ")
    path = Path(spath)
    if not path.exists():
        raise FileNotFoundError(f"The given path does not exist: '{path}'")
    if not path.is_file():
        raise FileExistsError(f"Given file path does not point to a file: '{path}'")
    save_gephi_path(path)
    return path

def save_gephi_path(path : Path):
    """
    Saves the path to the Gephi executable into the preference file.
    """
    param_path = preferences_dir / "path_to_gephi.txt"
    with param_path.open("w") as f:
        f.write(f"{path}")

def infer_gephi_path() -> Path:
    """
    Tries to find the path to Gephi. Raises an exception none of them was accepted.
    """
    ok = False
    p = get_gephi_path()
    if p:
        return p
    for p in search_gephi_paths():
        return p
    if not ok:
        return ask_user_for_gephi_path()
    raise RuntimeError("Could not find path to Gephi")





del Path, Iterator, sha3_512