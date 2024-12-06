"""
This module defines some useful tools for MetaGraphs.
"""

from typing import Iterable, Iterator, Literal, overload, TYPE_CHECKING
if TYPE_CHECKING:
    from .metagraph import FrozenMetaGraph
from ...bakery.source.graph import Arrow, Edge, Vertex
from functools import cache

__all__ = ["ontology", "check_ontological_validity", "constrained_ontological_relations"]





@cache
def ontology(*, just_parents : bool = False) -> "FrozenMetaGraph":
    """
    Returns the ontology structure graph of BAGUETTE. It contains all the possible entities and relations in BAGUETTE.
    """
    if not isinstance(just_parents, bool):
        raise TypeError(f"Expected bool, got '{type(just_parents).__name__}'")
    from itertools import product
    from functools import partial

    from ...bakery.source.graph import Arrow, Edge, Vertex
    from ...bakery.source.types.utils import relation_types, relations, entities
    from .metagraph import FrozenMetaGraph, MetaArrow, MetaEdge, MetaGraph, MetaVertex

    def isolate_parents[T](cls : tuple[type[T], ...]) -> tuple[type[T], ...]:
        scls = set(cls)
        return tuple(u for u in scls if not any(issubclass(u, v) and v is not u for v in scls))

    relation_matrix : dict[type[Vertex], dict[type[Vertex], set[type[Edge]]]] = {U : {V : set() for V in entities()} for U in entities()}

    for R in relations():
        for U1, V1 in relation_types(R):
            for U2 in filter(lambda U2 : issubclass(U2, U1), relation_matrix):
                for V2 in filter(lambda V2 : issubclass(V2, V1), relation_matrix[U1]):
                    relation_matrix[U2][V2].add(R)

    condensed_relation_matrix : dict[tuple[type[Vertex], ...], dict[tuple[type[Vertex], ...], set[type[Edge]]]] = {(U, ) : {(V, ) : relation_matrix[U][V] for V in relation_matrix[U]} for U in relation_matrix}

    def distance_to_class[T](C : type[T], ref : type[T]) -> int | float:
        if not issubclass(C, ref):
            return float("inf")
        return min(distance_to_class(B, ref) for B in C.__bases__)
    
    distance_to_vertex = partial(distance_to_class, ref = Vertex)
    distance_to_edge = partial(distance_to_class, ref = Edge)

    changed = True
    while changed:
        changed = False
        for U1, U2 in product(condensed_relation_matrix, repeat=2):
            if U1 is not U2:
                if condensed_relation_matrix[U1] == condensed_relation_matrix[U2] and all(condensed_relation_matrix[U][U1] == condensed_relation_matrix[U][U2] for U in condensed_relation_matrix):
                    U12 = tuple(sorted(U1 + U2, key=distance_to_vertex))
                    for U in condensed_relation_matrix:
                        condensed_relation_matrix[U].pop(U1)
                        entry = condensed_relation_matrix[U].pop(U2)
                        condensed_relation_matrix[U][U12] = entry
                    condensed_relation_matrix.pop(U1)
                    row = condensed_relation_matrix.pop(U2)
                    condensed_relation_matrix[U12] = row
                    changed = True
                    break

    mg = MetaGraph()
    translation_table : dict[tuple[type[Vertex], ...], MetaVertex] = {}
    edges : dict[tuple[MetaVertex, MetaVertex], set[type[Edge]]] = {}

    for U in condensed_relation_matrix:
        for V in condensed_relation_matrix[U]:
            with mg:
                A = tuple(sorted((e for e in condensed_relation_matrix[U][V] if issubclass(e, Arrow)), key = distance_to_edge))
                E = (e for e in condensed_relation_matrix[U][V] if not issubclass(e, Arrow))
                if U in translation_table:
                    MU = translation_table[U]
                else:
                    MU = MetaVertex()
                    MU.cls = isolate_parents(U) if just_parents else U
                    translation_table[U] = MU
                if V in translation_table:
                    MV = translation_table[V]
                else:
                    MV = MetaVertex()
                    MV.cls = isolate_parents(V) if just_parents else V
                    translation_table[V] = MV
                if A:
                    MA = MetaArrow(MU, MV)
                    MA.cls = isolate_parents(A) if just_parents else A
                if (MV, MU) not in edges:
                    edges[MU, MV] = set(E)
                else:
                    edges[MV, MU].update(E)
    
    for (MU, MV), E in edges.items():
        if E:
            with mg:
                ME = MetaEdge(MU, MV)
                E = tuple(sorted(E, key = distance_to_edge))
                ME.cls = isolate_parents(E) if just_parents else E

    return FrozenMetaGraph(mg)

Vertex.register_subclass_hook(lambda cls : ontology.cache_clear())
Edge.register_subclass_hook(lambda cls : ontology.cache_clear())





@overload
def check_ontological_validity(src_cls : Iterable[type[Vertex]] | type[Vertex], dst_cls : Iterable[type[Vertex]] | type[Vertex], edge_cls : Iterable[type[Edge]] | type[Edge], *, oriented : bool = False) -> bool:
    ...

@overload
def check_ontological_validity(src_cls : Iterable[type[Vertex]] | type[Vertex], dst_cls : Iterable[type[Vertex]] | type[Vertex], edge_cls : Iterable[type[Arrow]] | type[Arrow], *, oriented : Literal[True]) -> bool:
    ...

@cache
def check_ontological_validity(src_cls : Iterable[type[Vertex]] | type[Vertex], dst_cls : Iterable[type[Vertex]] | type[Vertex], edge_cls : Iterable[type[Edge]] | type[Edge], *, oriented : bool = False) -> bool:
    """
    Given iterables of source Vertex classes, destination Vertex classes and Edge (and/or Arrow) classes, returns True if such a link could exist in the current ontology.
    It also accepts single classes instead of iterables.
    If oriented is False, src_cls and dst_cls are assumed commutable and edge_cls should only contain Arrow classes.
    """
    from typing import Iterable
    from ...bakery.source.graph import Arrow, Edge, Vertex
    from ...bakery.source.types.utils import relation_types

    if not isinstance(oriented, bool):
        raise TypeError(f"Expected bool for 'oriented', got '{type(oriented).__name__}'")
    if isinstance(src_cls, type) and issubclass(src_cls, Vertex):
        src_cls = (src_cls, )
    if isinstance(dst_cls, type) and issubclass(dst_cls, Vertex):
        dst_cls = (dst_cls, )
    if isinstance(edge_cls, type) and issubclass(edge_cls, Edge):
        edge_cls = (edge_cls, )

    if not isinstance(src_cls, Iterable) or not isinstance(dst_cls, Iterable) or not isinstance(edge_cls, Iterable):
        raise TypeError(f"Expected iterable or class, iterable or class and iterable or class, got '{type(src_cls).__name__}', '{type(dst_cls).__name__}' and '{type(edge_cls).__name__}'")
    src_cls, dst_cls, edge_cls = tuple(src_cls), tuple(dst_cls), tuple(edge_cls)
    for sc in src_cls:
        if not isinstance(sc, type):
            raise TypeError(f"Expected iterable of Vertex subclasses for 'src_cls', got a '{type(sc).__name__}'")
        if not issubclass(sc, Vertex):
            raise TypeError(f"Expected iterable of Vertex subclasses for 'src_cls', got class '{sc.__name__}'")
    for dc in dst_cls:
        if not isinstance(dc, type):
            raise TypeError(f"Expected iterable of Vertex subclasses for 'dst_cls', got a '{type(dc).__name__}'")
        if not issubclass(dc, Vertex):
            raise TypeError(f"Expected iterable of Vertex subclasses for 'dst_cls', got class '{dc.__name__}'")
    for ec in edge_cls:
        if not isinstance(ec, type):
            raise TypeError(f"Expected iterable of Edge subclasses for 'edge_cls', got a '{type(ec).__name__}'")
        if not issubclass(ec, Edge):
            raise TypeError(f"Expected iterable of Edge subclasses for 'edge_cls', got class '{ec.__name__}'")
        if oriented and not issubclass(ec, Arrow):
            raise TypeError(f"Expected iterable of Arrow subclasses for 'edge_cls' when 'oriented' is True, got class '{ec.__name__}'")
        
    groups = ((src_cls, dst_cls), ) if oriented else ((src_cls, dst_cls), (dst_cls, src_cls))
    for src_cls, dst_cls in groups:

        for ec in edge_cls:
            for s, d in relation_types(ec):
                if any(issubclass(sc, s) for sc in src_cls) and any(issubclass(dc, d) for dc in dst_cls):
                    return True

    return False

Vertex.register_subclass_hook(lambda cls : check_ontological_validity.cache_clear())
Edge.register_subclass_hook(lambda cls : check_ontological_validity.cache_clear())





class OntologicalRelationsGenerator[U : Vertex, V : Vertex, E : Edge]:

    """
    An iterable class to yield all the possible relation triples given some constrains on these relations.
    """

    __relation_hierarchy : list[type[Edge]] = []

    def __init__(self, src_cls : tuple[type[U], ...], dst_cls : tuple[type[V], ...], edge_cls : tuple[type[E], ...], subclasses : bool) -> None:
        def isolate_parents[T](cls : tuple[type[T], ...]) -> tuple[type[T], ...]:
            scls = set(cls)
            return tuple(u for u in scls if not any(issubclass(u, v) and v is not u for v in scls))
        self.__src = isolate_parents(src_cls)
        self.__dst = isolate_parents(dst_cls)
        self.__edge = isolate_parents(edge_cls)
        self.__subclasses = subclasses

    @staticmethod
    def reset_relation_hierarchy():
        from ...bakery.source.types.utils import relations
        from ...bakery.source.graph import Edge
        def distance_to_class[T](C : type[T], ref : type[T]) -> int:
            if not issubclass(C, ref):
                raise TypeError(f"Expected subclass of '{ref.__name__}', got '{C.__name__}'")
            return max((distance_to_class(B, ref) for B in C.__bases__ if issubclass(B, ref)), default = 0)
        OntologicalRelationsGenerator.__relation_hierarchy = [Edge] + sorted(relations(), key = lambda cls : distance_to_class(cls, Edge))

    def __iter__(self) -> Iterator[tuple[type[U], type[V], type[E]]]:
        from ...bakery.source.types.utils import relation_types
        if not self.__src or not self.__dst or not self.__edge:     # No starting class on at least one end: no possible relations
            return
        
        seen_relations : "set[tuple[type[Vertex], type[Vertex], type[Edge]]]" = set()
        for R_ref in self.__edge:
            seen_relation_types : "set[type[Edge]]" = set()
            for R in self.__relation_hierarchy:
                if issubclass(R, R_ref):
                    if self.__subclasses or not any(issubclass(R, R2) for R2 in seen_relation_types):
                        for U_ref, V_ref in relation_types(R):
                            if issubclass(U_ref, self.__src) and issubclass(V_ref, self.__dst):
                                if (relation := (U_ref, V_ref, R)) not in seen_relations:
                                    yield relation
                                    seen_relations.add(relation)
                                    seen_relation_types.add(R)
        
Vertex.register_subclass_hook(lambda cls : OntologicalRelationsGenerator.reset_relation_hierarchy())
Edge.register_subclass_hook(lambda cls : OntologicalRelationsGenerator.reset_relation_hierarchy())

        
        
        

@overload
def constrained_ontological_relations[U : Vertex, V : Vertex, E : Edge](src_cls : Iterable[type[U]] | type[U] = Vertex, dst_cls : Iterable[type[V]] | type[V] = Vertex, edge_cls : Iterable[type[E]] | type[E] = Edge, *, oriented : Literal[False] = False, subclasses : bool = False) -> OntologicalRelationsGenerator[U, V, E]:
    ...

@overload
def constrained_ontological_relations[U : Vertex, V : Vertex, A : Arrow](src_cls : Iterable[type[U]] | type[U] = Vertex, dst_cls : Iterable[type[V]] | type[V] = Vertex, edge_cls : Iterable[type[A]] | type[A] = Arrow, *, oriented : Literal[True], subclasses : bool = False) -> OntologicalRelationsGenerator[U, V, A]:
    ...

@cache
def constrained_ontological_relations[U : Vertex, V : Vertex, E : Edge](src_cls : Iterable[type[U]] | type[U] = Vertex, dst_cls : Iterable[type[V]] | type[V] = Vertex, edge_cls : Iterable[type[E]] | type[E] = Edge, *, oriented : bool = False, subclasses : bool = False) -> OntologicalRelationsGenerator[U, V, E]:
    """
    Generates all the relation type triples in the form (<source Vertex class>, <destination Vertex class>, <Edge class>) that satisfy the given constraining classes given as arguments.
    If oriented is True, only Arrow subclasses are matched.
    If subclasses is False, relations will only be yielded if no relation for which vertex and edge classes are superclasses was yielded before. Yields all matches otherwise.
    """
    from ...bakery.source.graph import Arrow, Edge, Vertex
    from typing import Iterable

    if not isinstance(oriented, bool):
        raise TypeError(f"Expected bool for 'oriented', got '{type(oriented).__name__}'")
    if not isinstance(subclasses, bool):
        raise TypeError(f"Expected bool for 'subclasses', got '{type(subclasses).__name__}'")
    if isinstance(src_cls, type) and issubclass(src_cls, Vertex):
        src_cls = (src_cls, )
    if isinstance(dst_cls, type) and issubclass(dst_cls, Vertex):
        dst_cls = (dst_cls, )
    if isinstance(edge_cls, type) and issubclass(edge_cls, Edge):
        edge_cls = (edge_cls, )

    if not isinstance(src_cls, Iterable) or not isinstance(dst_cls, Iterable) or not isinstance(edge_cls, Iterable):
        raise TypeError(f"Expected iterable or class, iterable or class and iterable or class, got '{type(src_cls).__name__}', '{type(dst_cls).__name__}' and '{type(edge_cls).__name__}'")
    src_cls, dst_cls, edge_cls = tuple(src_cls), tuple(dst_cls), tuple(edge_cls)
    for sc in src_cls:
        if not isinstance(sc, type):
            raise TypeError(f"Expected iterable of Vertex subclasses for 'src_cls', got a '{type(sc).__name__}'")
        if not issubclass(sc, Vertex):
            raise TypeError(f"Expected iterable of Vertex subclasses for 'src_cls', got class '{sc.__name__}'")
    for dc in dst_cls:
        if not isinstance(dc, type):
            raise TypeError(f"Expected iterable of Vertex subclasses for 'dst_cls', got a '{type(dc).__name__}'")
        if not issubclass(dc, Vertex):
            raise TypeError(f"Expected iterable of Vertex subclasses for 'dst_cls', got class '{dc.__name__}'")
    for ec in edge_cls:
        if not isinstance(ec, type):
            raise TypeError(f"Expected iterable of Edge subclasses for 'edge_cls', got a '{type(ec).__name__}'")
        if not issubclass(ec, Edge):
            raise TypeError(f"Expected iterable of Edge subclasses for 'edge_cls', got class '{ec.__name__}'")
        if oriented and not issubclass(ec, Arrow):
            raise TypeError(f"Expected iterable of Arrow subclasses for 'edge_cls' when 'oriented' is True, got class '{ec.__name__}'")

    return OntologicalRelationsGenerator(src_cls, dst_cls, edge_cls, subclasses)

Vertex.register_subclass_hook(lambda cls : constrained_ontological_relations.cache_clear())
Edge.register_subclass_hook(lambda cls : constrained_ontological_relations.cache_clear())





del Iterable, Iterator, Literal, overload, Arrow, Edge, Vertex, cache