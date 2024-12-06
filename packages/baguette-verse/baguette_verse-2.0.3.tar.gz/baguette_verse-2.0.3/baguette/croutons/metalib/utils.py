"""
This module defines functions that get quite useful when building MetaGraphs.
"""

from pathlib import Path
from ..source.metagraph import MetaGraph, FrozenMetaGraph
from ...setup.preferences import preferences_dir

__all__ = ["import_env", "save", "load", "entries", "index", "remove", "export_MG", "import_MG"]





METALIB_DIRECTORY = preferences_dir / "metalib"





def import_env(d : dict):

    """
    Imports all the necessary classes for building MetaGraphs
    """

    from ...bakery.source import types as types_package
    from ...bakery.source.graph import Graph, Vertex, Edge, Arrow
    from ..source.metagraph import MetaGraph, MetaEdge, MetaArrow, MetaVertex
    from ...bakery.source.types.utils import entities, relations, relation_types, behavioral_packages, ontology 
    from types import ModuleType

    l = locals().copy()
    if "l" in l:
        l.pop("l")
    l.pop("d")
    l.pop("types_package")

    for name in dir(types_package):
        val = getattr(types_package, name)
        if isinstance(val, ModuleType):
            l[name] = val

    d.update(l)





def save(mg : MetaGraph, name : str):
    """
    Saves the given MetaGraph in the library with the given name.
    """
    from ..source.metagraph import MetaGraph, FrozenMetaGraph
    from pickle import dump

    if not isinstance(mg, MetaGraph) or not isinstance(name, str):
        raise TypeError("Expected MetaGraph, str, got " + repr(type(mg).__name__) + " and " + repr(type(name).__name__))
    if not isinstance(mg, FrozenMetaGraph):
        mg = FrozenMetaGraph(mg)
    
    path = METALIB_DIRECTORY / f"{name}.pyt"
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("wb") as f:
        dump(mg, f)





def load(name : str) -> FrozenMetaGraph:
    """
    Loads the MetaGraph with given name from the library.
    """
    from pickle import load

    if not isinstance(name, str):
        raise TypeError("Expected str, got " + repr(type(name).__name__))

    path = METALIB_DIRECTORY / f"{name}.pyt"

    if not path.is_file():
        raise FileNotFoundError("Given MetaGraph name does not exist in the library.")
    
    with path.open("rb") as f:
        return load(f)





def entries() -> list[str]:
    """
    Returns the names of all MetaGraphs existing in the library.
    """
    if not METALIB_DIRECTORY.is_dir():
        return []
    return [p.stem for p in METALIB_DIRECTORY.glob("*.pyt")]





def index() -> dict[FrozenMetaGraph, str]:
    """
    Returns the inverted metalib: a dictionary with MetaGraphs as keys and their names as values.
    """
    return {load(name) : name for name in entries()}





def remove(name : str):
    """
    Removes the given name from the MetaGraph library.
    """
    from os import remove

    if not isinstance(name, str):
        raise TypeError("Expected str, got " + repr(type(name).__name__))

    path = METALIB_DIRECTORY / f"{name}.pyt"

    if not path.is_file():
        raise FileNotFoundError("No such MetaGraph : " + repr(path))

    remove(path)





def export_MG(mg : MetaGraph, file : str | Path):
    """
    Exports the given MetaGraph to the given file.
    """
    from pathlib import Path
    from ..source.metagraph import FrozenMetaGraph
    if not isinstance(mg, MetaGraph):
        raise TypeError("Expected MetaGraph, path, got " + repr(type(mg).__name__) + " and " + repr(type(file).__name__))
    if not isinstance(mg, FrozenMetaGraph):
        mg = FrozenMetaGraph(mg)
    if isinstance(file, str):
        try:
            file = Path(file)
        except:
            raise ValueError("Invalid path : '{}'".format(file))
    if not isinstance(file, Path):
        raise TypeError("Expected MetaGraph, path, got " + repr(type(mg).__name__) + " and " + repr(type(file).__name__))
    from pickle import dump
    with file.open("wb") as f:
        dump(mg, f)
    




def import_MG(file : str | Path) -> FrozenMetaGraph:
    """
    Imports a MetaGraph from the given path.
    """
    from pathlib import Path
    if isinstance(file, str):
        try:
            file = Path(file)
        except:
            raise ValueError("Invalid path : '{}'".format(file))
    if not isinstance(file, Path):
        raise TypeError("Expected path, got " + repr(type(file).__name__))
    from pickle import load
    with file.open("rb") as f:
        return load(f)
    




del Path, MetaGraph, FrozenMetaGraph, preferences_dir