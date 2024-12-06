"""
This module contains an interface to read matches from a file as a sequence without loading it first entirely.
"""

from collections.abc import Sequence
from typing import Iterator, overload
from .abc import BytesSeekable
from .caching_pickle import CachingUnpickler
from ..croutons.source.metagraph import FrozenMetaGraph





class MatchFileSequence(Sequence[FrozenMetaGraph.Match]):

    """
    Given a file object, reads matches with random access.
    Not quite as nice as a sequence (no reversing and accessing random elements in the middle of the sequence may be long at first).
    """

    from collections import OrderedDict as __OrderedDict
    from bz2 import BZ2File as __BZ2File
    from io import SEEK_END as __SEEK_END
    from itertools import islice as __islice
    from .sub_file import SectorReader as __SectorReader
    from ..croutons.source.metagraph import FrozenMetaGraph as __FrozenMetaGraph

    CACHE_MAX_SIZE = 2 ** 16

    def __init__(self, file : __SectorReader, unpickler : CachingUnpickler) -> None:
        file.seek(0)
        metadata_size = int.from_bytes(file.read(8), "little")
        with MatchFileSequence.__BZ2File(MatchFileSequence.__SectorReader(file, 8, 8 + metadata_size), "rb") as f: # type: ignore
            unpickler.set_input(f)
            metadata : "tuple[dict[FrozenMetaGraph, list[int]], int]" = unpickler.load()
            index, self.__bytes_size = metadata
        self.__positions : "list[tuple[int, FrozenMetaGraph]]" = []
        for mg, mg_positions in index.items():
            self.__positions.extend(((pos, mg) for pos in mg_positions))
        self.__positions.sort(key = lambda t : t[0])
        self.__index  : "dict[FrozenMetaGraph, list[int]]" = {mg : [] for mg in index}
        for i, (mg_positions, mg) in enumerate(self.__positions):
            self.__index.setdefault(mg, []).append(i)
        self.__file = MatchFileSequence.__BZ2File(MatchFileSequence.__SectorReader(file, 8 + metadata_size), "rb") # type: ignore
        self.__unpickler = unpickler
        self.__cache : "MatchFileSequence.__OrderedDict[int, FrozenMetaGraph.Match]" = MatchFileSequence.__OrderedDict()
        self.__enabled = True

    @property
    def patterns(self) -> set[FrozenMetaGraph]:
        """
        The MetaGraphs that had at least one match.
        """
        return set(self.__index)

    def disable(self):
        """
        Disables the object when the BAGUETTE file is modified.
        """
        self.__enabled = False

    def __add_to_cache(self, value : FrozenMetaGraph.Match, pos : int):
        """
        Internal function to add an entry to the cache.
        """
        if pos not in self.__cache:
            self.__cache[pos] = value
            if len(self.__cache) > MatchFileSequence.CACHE_MAX_SIZE:
                self.__cache.popitem(False)

    def __len__(self) -> int:
        """
        Implements len(self).
        """
        return len(self.__positions)
    
    def __iter__(self) -> Iterator[FrozenMetaGraph.Match]:
        """
        Implements iter(self). Yields all the Matches of the file.
        """
        for i, (pos, mg) in enumerate(self.__positions):
            if not self.__enabled:
                raise RuntimeError("BAGUETTE file has changed")
            if i in self.__cache:
                yield self.__cache[i]
            else:
                self.__file.seek(pos)
                self.__unpickler.set_input(self.__file)
                res = self.__unpickler.load()
                self.__add_to_cache(res, i)
                yield res

    def __reversed__(self) -> Iterator[FrozenMetaGraph.Match]:
        """
        Implements reversed(self). Yields all the Matches of the file in reversed order.
        """
        i = len(self.__positions)
        for pos, mg in reversed(self.__positions):
            i -= 1
            if not self.__enabled:
                raise RuntimeError("BAGUETTE file has changed")
            if i in self.__cache:
                yield self.__cache[i]
            else:
                self.__file.seek(pos)
                self.__unpickler.set_input(self.__file)
                res = self.__unpickler.load()
                self.__add_to_cache(res, i)
                yield res



    class PatternView(Sequence[FrozenMetaGraph.Match]):

        """
        A view on the matches of a specific FrozenMetaGraph pattern.
        """

        def __init__(self, pattern : FrozenMetaGraph, master : "MatchFileSequence", positions : list[int]) -> None:
            self.__pattern = pattern
            self.__master = master
            self.__positions = positions

        @property
        def pattern(self) -> FrozenMetaGraph:
            """
            The FrozenMetaGraph that this view is on.
            """
            return self.__pattern
        
        def __len__(self) -> int:
            return len(self.__positions)
        
        def __iter__(self) -> Iterator[FrozenMetaGraph.Match]:
            yield from (self.__master[i] for i in self.__positions)
        
        def __reversed__(self) -> Iterator[FrozenMetaGraph.Match]:
            yield from (self.__master[i] for i in reversed(self.__positions))

        @overload
        def __getitem__(self, i : int) -> FrozenMetaGraph.Match:
            ...

        @overload
        def __getitem__(self, i : slice) -> tuple[FrozenMetaGraph.Match, ...]:
            ...

        def __getitem__(self, i : int | slice) -> FrozenMetaGraph.Match | tuple[FrozenMetaGraph.Match, ...]:
            if isinstance(i, int):
                if i < 0:
                    i -= len(self)
                if not 0 <= i < len(self):
                    raise IndexError(f"PatternView index out of range: {i}")
                return self.__master[i]
            elif isinstance(i, slice):
                return tuple(self[i] for i in range(len(self.__positions))[i])
            else:
                raise TypeError(f"Expected int or slice, got '{type(i).__name__}'")


    @overload
    def __getitem__(self, i : int) -> FrozenMetaGraph.Match:
        ...

    @overload
    def __getitem__(self, i : slice) -> tuple[FrozenMetaGraph.Match, ...]:
        ...

    @overload
    def __getitem__(self, i : FrozenMetaGraph) -> PatternView:
        ...
    
    def __getitem__(self, i : int | slice | FrozenMetaGraph) -> FrozenMetaGraph.Match | tuple[FrozenMetaGraph.Match, ...] | PatternView:
        """
        Implements self[i]. Returns the i-th Match. 
        """
        if isinstance(i, int):
            if i < 0:
                i -= len(self)
            if not 0 <= i < len(self):
                raise IndexError(f"MatchFileSequence index out of range: {i}")
            if not self.__enabled:
                raise RuntimeError("BAGUETTE file has changed")
            if i in self.__cache:
                return self.__cache[i]
            pos = self.__positions[i][0]
            self.__file.seek(pos)
            self.__unpickler.set_input(self.__file)
            res = self.__unpickler.load()
            self.__add_to_cache(res, i)
            return res
        elif isinstance(i, slice):
            return tuple(self[i] for i in range(len(self.__positions))[i])
        elif isinstance(i, MatchFileSequence.__FrozenMetaGraph):
            return MatchFileSequence.PatternView(i, self, self.__index.get(i, []))
        else:
            raise TypeError(f"Expected int, slice or FrozenMetaGraph, got '{type(i).__name__}'")
    
    



del Sequence, Iterator, overload, BytesSeekable, CachingUnpickler, FrozenMetaGraph