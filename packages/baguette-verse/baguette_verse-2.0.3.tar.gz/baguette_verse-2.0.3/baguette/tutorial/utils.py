"""
This script will copy the content of reports.zip into the given destination folder.
(Archive's password is b"infected")
"""

from typing import Any, Iterator
import zipfile
from pathlib import Path

__all__ = ["data_file", "state_file", "data_filesystem", "extract_subfolder", "walk_archive", "states", "get_state", "set_state", "warn_wrong_state", "next_state", "create_command_line"]





data_file = zipfile.ZipFile(Path(__file__).parent.parent / "data" / "tutorial.zip")
data_file.setpassword(b"infected")

state_file = Path("~/.baguette").expanduser().absolute() / "state.txt"

data_filesystem = zipfile.Path(data_file)

def extract_subfolder(source : zipfile.Path, destination : Path) -> Iterator[Path]:
    """
    Decompresses a zip source folder (path should be relative to the data archive) into the destination folder.
    Returns the number of files extracted.
    """
    from zipfile import Path as ZPath

    if not source.exists():
        raise FileNotFoundError(f"Could not find file '{source}' in data archive")
    if source.is_file():
        raise FileExistsError(f"Member '{source}' is a file in the data archive")
    
    if destination.exists() and not destination.is_dir():
        raise FileExistsError(f"'{destination}' destination folder exists and is not a directory")

    def deep_iter(path : ZPath) -> list[ZPath]:
        if path.is_file():
            return [path]
        elif path.is_dir():
            l = [path]
            for pi in path.iterdir():
                l.extend(deep_iter(pi))
            return l
        else:
            return []
    
    for file_path in deep_iter(source):
        relative = str(file_path)[len(str(source)):]
        dest = destination / relative
        if file_path.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            yield dest
        elif file_path.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open("wb") as f:
                f.write(file_path.read_bytes())
            yield dest





def walk_archive(source : zipfile.Path = zipfile.Path(data_file), *, leaves_only : bool = False) -> Iterator[zipfile.Path]:
    """
    Yields all the items in the data archive, starting from the given path.
    """
    if source.is_file():
        yield source
    elif source.is_dir():
        if not leaves_only:
            yield source
        for pi in source.iterdir():
            yield from walk_archive(pi)





# __states should be ordered and describe the tutorial scenario.
__states = {
    "not started" : "The tutorial has not been started yet.",
    "fetching samples" : "The user should use the command line 'baguette.tutorial.samples -h' to get report samples.",
    "preparing" : "The user should use 'prepare' to put the execution reports into empty BAGUETTE files.\nOnce done, the user should use 'baguette.tutorial' for next step.",
    "baking" : "The user should use 'bake' to start baking BAGUETTEs from the report samples.\nOnce done, the user should use 'baguette.tutorial' for next step.",
    "baked" : "The user has studied the freshly baked BAGUETTEs and is ready to learn about toasting.\nUse 'baguette.tutorial' for next step.",
    "metalib" : "The user should be writting a MetaGraph.\nOnce it has been saved, use 'baguette.tutorial' to continue.",
    "toasting" : "The user should be toasting BAGUETTEs using the newly defined MetaGraph.\nUse 'baguette.tutorial' once done.",
    "finished" : "The user has completed the tutorial.\nUse 'baguette.tutorial.reset' to do it again."
}

def states() -> dict[str, str]:
    """
    Returns the list of possible states of the tutorial.
    """
    return __states.copy()

def get_state() -> str:
    """
    Returns the current state of the tutorial.
    """
    if not state_file.exists():
        return list(__states)[0]
    state = state_file.read_text()
    if state not in __states:
        raise RuntimeError(f"Unregistered tutorial state: '{state}'")
    return state

def set_state(state : str):
    """
    Sets the state of the tutorial.
    """
    if state not in __states:
        raise RuntimeError(f"Unregistered tutorial state: '{state}'")
    state_file.write_text(state)

def next_state(state : str) -> bool:
    """
    Moves to next state if the current state is the given state.
    Returns True on success, False otherwise.
    """
    if get_state() == state:
        l = list(__states)
        i = l.index(state)
        n_state = l[(i + 1) % len(l)]
        set_state(n_state)
        return True
    return False

def warn_wrong_state(expected_state : str) -> bool:
    """
    Checks that the tutorial is in the given expected stated. If not, prints a warning about that.
    Returns True of the tutorial is in the right state, False otherwise.
    """
    if get_state() == expected_state:
        return True
    print("error : tutorial already started. Use 'baguette.tutorial.reset' to restart the tutorial.")
    print(f"Tutorial is currently at step : '{get_state()}' : {__states[get_state()]}")
    return False





def create_command_line(executable : Any, *args : Any) -> str:
    """
    Encodes the given arguments and joins them to form a command line for the system shell.
    Returns a string of what the command line would look like (starts with '$' on Linux and '>' on Windows).
    """
    from sys import platform
    if platform == "win32":
        def wrap(arg : "Any") -> str:
            sarg = str(arg)
            requires_quotes = False
            sarg_2 = sarg.replace('"', '`"')
            requires_quotes = requires_quotes or sarg != sarg_2
            sarg = sarg_2.replace('`', '``')
            requires_quotes = requires_quotes or sarg != sarg_2
            if " " in sarg or requires_quotes:
                sarg = f'"{sarg}"'
            return sarg
        wrapped_executable = wrap(executable)
        if wrapped_executable.startswith('"') or wrapped_executable.startswith("'"):
            wrapped_executable = f"& {wrapped_executable}"
        return f"> {wrapped_executable}" + (" " if args else "") + " ".join(wrap(arg) for arg in args)
    else:
        def wrap(arg : "Any") -> str:
            sarg = str(arg)
            requires_quotes = False
            sarg_2 = sarg.replace('"', '\\"')
            requires_quotes = requires_quotes or sarg != sarg_2
            sarg = sarg_2.replace('\\', '\\')
            requires_quotes = requires_quotes or sarg != sarg_2
            if " " in sarg or requires_quotes:
                sarg = f'"{sarg}"'
            return sarg
        return f"$ {wrap(str(executable))}" + (" " if args else "") + " ".join(wrap(str(arg)) for arg in args)






del zipfile, Path, Any