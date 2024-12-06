"""
This module defines basic graph filters. Use them to reduce the size of the graph by only keeping specific edges.
To be used with 'bake', all custom Filters must be defined in this file!
"""

from typing import Callable, Iterable, LiteralString
from .graph import Edge, Vertex, Graph
from Viper.meta.iterable import InstanceReferencingClass
from .utils import chrono
from .types.registry.entities import Key, KeyEntry, Handle
from functools import cache
from Viper.collections.isomorph import IsoSet

__all__ = ["Filter", "significant_call_only", "no_data_nodes", "no_simple_imports", "no_handle_nodes", "injected_threads_only", "significant_processes_only", "modified_registry_only"]





class FilterSystem:

    """
    A simple class used to create a complete Graph filter.
    """

    def __init__(self, g : Graph) -> None:
        self.__graph = g

    @property
    def graph(self) -> Graph:
        """
        The Graph being currently filtered.
        """
        return self.__graph

    def edge_filter_function(self, e : Edge) -> bool:
        """
        Called to tell whether or not an Edge of a Graph should be filtered or not.
        """
        return True
    
    def vertex_filter_function(self, v : Vertex) -> bool:
        """
        Called to tell whether or not a Vertex of a Graph should be filtered or not.
        """
        return True
    




class Filter[Name : LiteralString](metaclass = InstanceReferencingClass):

    """
    A filter object for graphs.
    """

    from itertools import chain as __chain

    __filter_system_classes__ : dict[Name, "Filter[Name]"] = {}

    @staticmethod
    def enumerate() -> dict[Name, "Filter[Name]"]:
        """
        Returns a dictionary of all the Filters indexed by their names.
        """
        return Filter.__filter_system_classes__.copy() # type: ignore

    def __init__(self, filter_system : type[FilterSystem], name : Name) -> None:
        if not isinstance(filter_system, type) or not isinstance(name, str):
            raise TypeError(f"Expected type, str got '{type(filter_system).__name__}' and '{type(name).__name__}'")
        if not issubclass(filter_system, FilterSystem):
            raise ValueError(f"Expected subclass of FilterSystem, got '{filter_system}'")
        self.__filter_system_classes__[name] = self
        self.__filter_system = filter_system
        self.__name = name

    @property
    def name(self) -> Name:
        """
        The name of this filter.
        """
        return self.__name
    
    @property
    def doc(self) -> str:
        """
        The documentation of this filter.
        """
        if (doc := self.__filter_system.__doc__) is None:
            raise ValueError(f"Could not find documentation for FilterSystem '{self.__filter_system.__name__}'")
        return doc
    
    def __call__(self, g : Graph) -> Iterable[Edge | Vertex]:
        """
        Implements self(iterable). Filters the given Graph, yielding all accepted edges and vertices.
        """
        from .graph import Edge, Vertex
        if not isinstance(g, Graph):
            raise TypeError("Expected Grpah, got " + repr(type(g).__name__))
        filter = self.__filter_system(g)
        for x in g:
            if isinstance(x, Edge):
                if filter.edge_filter_function(x):
                    yield x
            elif isinstance(x, Vertex):
                if filter.vertex_filter_function(x):
                    yield x
            else:
                raise TypeError("Expected iterable of Edges or Vertices, got a " + repr(type(x).__name__))
    
    @chrono
    def apply[G : Graph](self, g : G) -> G:
        """
        Applies the filter to the given graph, returning a new one.
        """
        from .graph import Graph
        if not isinstance(g, Graph):
            raise TypeError("Expected Graph, got " + repr(type(g).__name__))
        filter = self.__filter_system(g)
        return type(g)(Filter.__chain((v for v in g.vertices if filter.vertex_filter_function(v)), (e for e in g.edges if filter.edge_filter_function(e))))





# Here we will define some basic filters:

class ImportantCallFilter(FilterSystem):

    """
    Filters out the (API) Call vertices that had no concrete effect on the BAGUETTE Graph (i.e. those not linked to anything other than other Call vertices).
    """

    def vertex_filter_function(self, v: Vertex) -> bool:
        from .types.execution import Call
        if not isinstance(v, Call):
            return True
        else:
            for v in v.neighbors():
                if not isinstance(v, Call) and v in self.graph:
                    return True
            return False

class DataNodesFilter(FilterSystem):

    """
    Filters out all the Data vertices.
    """

    def vertex_filter_function(self, v: Vertex) -> bool:
        from .types.data import Data
        return not isinstance(v, Data)

class SimpleImportsFilter(FilterSystem):

    """
    Filters out all the Import vertices that are not just simple imports (i.e. those for which the file is opened for example).
    """

    def vertex_filter_function(self, v: Vertex) -> bool:
        from .types.imports import Import
        from .types.execution import Process
        return not isinstance(v, Import) or bool([u for u in v.neighbors() if not isinstance(u, Process) and u in self.graph])

class NoHandlesFilter(FilterSystem):

    """
    Filters out the (file/registry) Handles/Socket vertices except the handles to a file being executed by a Process.
    """

    def vertex_filter_function(self, v: Vertex) -> bool:
        from .types.filesystem import Handle as FileHandle
        from .types.network import Socket
        from .types.registry import Handle as KeyHandle
        from .types.execution import Process
        if not isinstance(v, FileHandle | Socket | KeyHandle):
            return True
        if isinstance(v, Socket | KeyHandle):
            return False
        if v.file and v.file in self.graph:
            for u in v.file.neighbors():
                if isinstance(u, Process) and u in self.graph:
                    return True
        return False
    
class InjectedThreadsFilter(FilterSystem):
    
    """
    Filters out the Thread vertices that are not threads injected into other processes.
    """

    def vertex_filter_function(self, v: Vertex) -> bool:
        from .types.execution import Thread, Process
        return not isinstance(v, Thread) or len([u for u in v.neighbors() if isinstance(u, Process)]) > 1

class SignificantProcessFilter(FilterSystem):
    
    """
    Filters out the Process vertices that could not be traced and are not a root process of the analysis.
    """

    def vertex_filter_function(self, v: Vertex) -> bool:
        from .types.execution import Process
        from .types.network import Host

        if not isinstance(v, Process):
            return True

        def test_process_vertex(v : Process) -> bool:
            return bool([u for u in v.neighbors() if not isinstance(u, (Process, Host))]) or v.parent_process == None
            
        return test_process_vertex(v) or any(self.vertex_filter_function(u) for u in v.children_processes)
    
class ChangedRegistryFilter(FilterSystem):

    """
    Filters out the registry Key (and related) vertices that only represent reading operations.
    """

    def __init__(self, g: Graph) -> None:
        super().__init__(g)
        from Viper.collections.isomorph import IsoSet
        from .types.registry import KeyEntry, ChangesTowards, SetsEntry, DeletesEntry
        self.__changing_entries : "IsoSet[KeyEntry]" = IsoSet()
        self.__changing_keys : "IsoSet[Key]" = IsoSet()
        for u in self.graph.vertices:
            if isinstance(u, KeyEntry) and any(isinstance(e, ChangesTowards | SetsEntry | DeletesEntry) for e in u.edges):
                self.__changing_entries.add(u)
                k = u.key
                while k:
                    self.__changing_keys.add(k)
                    k = k.parent_key

    def vertex_filter_function(self, v: Vertex) -> bool:
        from .types.registry import Key, KeyEntry, Handle

        if not isinstance(v, Key | KeyEntry | Handle):
            return True
        elif isinstance(v, Handle):
            return v.key in self.__changing_keys
        elif isinstance(v, Key):
            return v in self.__changing_keys
        elif isinstance(v, KeyEntry):
            return v in self.__changing_entries
    




significant_call_only = Filter(ImportantCallFilter, "significant_call_only")
no_data_nodes = Filter(DataNodesFilter, "no_data_nodes")
no_simple_imports = Filter(SimpleImportsFilter, "no_simple_imports")
no_handle_nodes = Filter(NoHandlesFilter, "no_handle_nodes")
injected_threads_only = Filter(InjectedThreadsFilter, "injected_threads_only")
significant_processes_only = Filter(SignificantProcessFilter, "significant_processes_only")
modified_registry_only = Filter(ChangedRegistryFilter, "modified_registry_only")





del Callable, Iterable, LiteralString, Edge, Vertex, Graph, InstanceReferencingClass, chrono, Key, KeyEntry, Handle, cache, IsoSet
del ImportantCallFilter, DataNodesFilter, SimpleImportsFilter, NoHandlesFilter, InjectedThreadsFilter, SignificantProcessFilter, ChangedRegistryFilter