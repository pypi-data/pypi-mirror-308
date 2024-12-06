"""
This module adds some useful functions and classes for the compilation of BAGUETTE graphs.
"""

import pathlib
from threading import Thread
from typing import TYPE_CHECKING, Any, Callable, Iterable, Iterator, Set

from Viper.debugging.chrono import Chrono
from Viper.collections.isomorph import IsoSet

from .graph import Edge, Vertex
if TYPE_CHECKING:
    from .build import Builder

__all__ = ["chrono", "path_factory", "is_path", "parse_command_line", "active_builders", "active_builder"]





chrono = Chrono()
chrono.enabled = False





def path_factory(path : str) -> pathlib.PurePath:
    """
    Returns the correct path factory class for the given graph (either WindowsPurePath or PosixPurePath).
    """
    from pathlib import PurePosixPath, PureWindowsPath

    from .graph import Graph
    platform = "windows"
    for g, _ in Graph.graphs_status():
        if "platform" in g.data:
            platform = g.data["platform"].lower()
            break
    if "windows" in platform:
        return PureWindowsPath(path)
    else:
        return PurePosixPath(path)


def is_path(s : str) -> bool:
    """
    Returns True if the given string represents a path for the current platform.
    """
    from pathlib import PurePosixPath, PureWindowsPath

    from .graph import Graph
    platform = Graph.active_graphs()[-1].data["platform"].lower() if Graph.active_graphs() else "windows"
    if "windows" in platform:
        forbidden = set("<>\"|?*")
        if forbidden.intersection(s):           # Contains characters that are forbidden in Windows paths.
            return False
        if s.startswith("-") or s.startswith("/"):  # Could be a path, but it is more likely to be flag
            return False
        try:
            if PureWindowsPath(s).is_reserved():
                return False
            return True
        except:
            return False
    else:
        if s.startswith("-"):                       # Could be a path, but it is more likely to be flag
            return False
        try:
            if PurePosixPath(s).is_reserved():
                return False
            return True
        except:
            return False
        

def parse_command_line(cmd : str, *, executable : str | None = None) -> list[str]:
    """
    Parses command line with the syntax of the current platform's shell. Returns the argument vector.
    If given, the executable argument helps parsing commands with a single argument given without quotes.
    """
    import re

    from .graph import Graph
    
    if not cmd:
        if executable:
            return [executable]
        return []

    platform = Graph.active_graphs()[-1].data["platform"].lower() if Graph.active_graphs() and "platform" in Graph.active_graphs()[-1].data else "windows"
    if "windows" not in platform:
        RE_CMD_LEX = r'''"((?:\\["\\]|[^"])*)"|'([^']*)'|(\\.)|(&&?|\|\|?|\d?\>|[<])|([^\s'"\\&|<>]+)|(\s+)|(.)'''
    else:
        RE_CMD_LEX = r'''"((?:""|\\["\\]|[^"])*)"?()|(\\\\(?=\\*")|\\")|(&&?|\|\|?|\d?>|[<])|([^\s"&|<>]+)|(\s+)|(.)'''

    args : list[str] = []
    accu = None   # collects pieces of one arg
    for qs, qss, esc, pipe, word, white, fail in re.findall(RE_CMD_LEX, cmd):
        if word:
            pass   # most frequent
        elif esc:
            word = esc[1]
        elif white or pipe:
            if accu is not None:
                args.append(accu)
            if pipe:
                args.append(pipe)
            accu = None
            continue
        elif fail:
            raise ValueError("invalid or incomplete shell string")
        elif qs:
            word = qs.replace('\\"', '"').replace('\\\\', '\\')
            if "windows" in platform:
                word = word.replace('""', '"')
        else:
            word = qss   # may be even empty; must be last

        accu = (accu or '') + word

    if accu is not None:
        args.append(accu)

    if executable is not None and args:
        parsed_executable = path_factory(args[0])
        executable_path = path_factory(executable)

        if "windows" not in platform and parsed_executable.stem != executable_path.stem:
            for i, arg in enumerate(args):
                try:
                    p = path_factory(arg)
                    if p.stem == executable_path.stem:
                        return [" ".join(args[:i + 1])] + parse_command_line(" ".join(args[i + 1:]))
                except:
                    pass

        elif "windows" in platform and parsed_executable.stem.lower() != executable_path.stem.lower():
            for i, arg in enumerate(args):
                try:
                    p = path_factory(arg)
                    if p.stem.lower() == executable_path.stem.lower():
                        return [" ".join(args[:i + 1])] + parse_command_line(" ".join(args[i + 1:]))
                except:
                    pass

    return args


active_builders : dict[Thread, "Builder"] = {}


def active_builder() -> "Builder | None":
    from threading import current_thread
    return active_builders.get(current_thread())





del pathlib, Any, Callable, Iterable, Iterator, Set, Chrono, Edge, Vertex, IsoSet