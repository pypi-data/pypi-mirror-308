"""
This module defines some useful functions for manipulating the BAGUETTE graph typing system.
"""

from functools import cache
from types import ModuleType
from .. import types as type_package
from ..graph import Edge, Vertex

__all__ = ["entities", "relations", "relation_types", "behavioral_packages", "ontology"]





@cache
def entities(mod : ModuleType | None = None) -> set[type[Vertex]]:
    """
    Returns the list of available Vertex types available in a given module or package (recursively). Defaults to the BAGUETTE's types package.
    """
    from ..graph import Vertex
    from ....croutons.source.metagraph import MetaVertex
    from types import ModuleType

    if mod is None:
        cls : "set[type[Vertex]]" = set()
        to_see = {Vertex}
        while to_see:
            c = to_see.pop()
            if not issubclass(c, MetaVertex) and c not in cls:
                to_see.update(c.__subclasses__())
                if c.__module__ != Vertex.__module__:
                    cls.add(c)
        return cls
    
    if not isinstance(mod, ModuleType):
        raise TypeError("Expected module or package or None, got " + repr(type(mod).__name__))

    type_set : set[type[Vertex]] = set()
    package_name = mod.__name__

    for name in dir(mod):
        value = getattr(mod, name)
        if isinstance(value, type) and issubclass(value, Vertex):
            type_set.add(value)
        elif isinstance(value, ModuleType):
            name = value.__name__.rpartition(".")[0]
            if name == package_name:
                type_set.update(entities(value))
    
    return type_set

Vertex.register_subclass_hook(lambda cls : entities.cache_clear())





@cache
def relations(mod : ModuleType | None = None) -> set[type[Edge]]:
    """
    Returns the list of available Edge and Arrow types available in a given module or package (recursively). Defaults to the BAGUETTE's types package.
    """
    from ..graph import Edge
    from ....croutons.source.metagraph import MetaEdge
    from types import ModuleType
    
    if mod is None:
        cls : "set[type[Edge]]" = set()
        to_see = {Edge}
        while to_see:
            c = to_see.pop()
            if not issubclass(c, MetaEdge) and c not in cls:
                to_see.update(c.__subclasses__())
                if c.__module__ != Edge.__module__:
                    cls.add(c)
        return cls

    if not isinstance(mod, ModuleType):
        raise TypeError("Expected module or package or None, got " + repr(type(mod).__name__))

    type_set : set[type[Edge]] = set()
    package_name = mod.__name__

    for name in dir(mod):
        value = getattr(mod, name)
        if isinstance(value, type) and issubclass(value, Edge):
            type_set.add(value)
        elif isinstance(value, ModuleType):
            name = value.__name__.rpartition(".")[0]
            if name == package_name:
                type_set.update(relations(value))
    
    return type_set

Edge.register_subclass_hook(lambda cls : relations.cache_clear())





def behavioral_packages() -> dict[str, ModuleType]:
    """
    Returns a dictionary holding all the avaiable behavioral packages in the form {name : package}.
    Such packages can be used with types() and relations().
    """
    from .. import types as type_package
    from types import ModuleType

    index = {}
    package_name = type_package.__name__
    for name in dir(type_package):
        value = getattr(type_package, name)
        if isinstance(value, ModuleType):
            pname, _, mname = value.__name__.rpartition(".")
            if pname == package_name and mname in type_package.__all__:
                index[mname] = value

    return index





@cache
def relation_types(edge_class : type[Edge]) -> set[tuple[type[Vertex], type[Vertex]]]:
    """
    Given an Edge or Arrow subclass, gives the best type hints for the source and destination vertices.
    Defaults to (Vertex, Vertex) when no annotations exist.
    """
    from typing import get_type_hints
    from types import UnionType
    from ..graph import Edge, Vertex

    if not isinstance(edge_class, type) or not issubclass(edge_class, Edge):
        raise TypeError("Expected Edge subclass, got " + repr(edge_class))

    hints = get_type_hints(edge_class)
    S, D = hints.get("source", Vertex), hints.get("destination", Vertex)
    if isinstance(S, UnionType):
        S = tuple(S.__args__)
    else:
        S = (S, )
    if isinstance(D, UnionType):
        D = tuple(D.__args__)
    else:
        D = (D, )
    return {(s, d) for s in S for d in D}

Vertex.register_subclass_hook(lambda cls : relation_types.cache_clear())
Edge.register_subclass_hook(lambda cls : relation_types.cache_clear())





def ontology(*, just_parents : bool = False):
    """
    A dynamic clone of 'baguette.croutons.source.utils.ontology'.
    """
    if not isinstance(just_parents, bool):
        raise TypeError(f"Expected bool, got '{type(just_parents).__name__}'")
    from ....croutons.source.utils import ontology
    return ontology(just_parents=just_parents)
    




del cache, ModuleType, type_package, Edge, Vertex