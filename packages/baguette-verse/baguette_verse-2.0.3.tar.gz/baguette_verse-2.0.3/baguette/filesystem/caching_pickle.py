"""
This module adds a Pickler and an Unpickler subclasses that also store a common cache separately and supports reading/writing to different files.
"""

from pickle import Pickler, Unpickler
from typing import Any
from .abc import BytesReadable, BytesWritable

__all__ = ["CachingPickler", "CachingUnpickler"]





class CachingPickler(Pickler):

    """
    This subclass of pickler uses a cache (anything) to reference some object instead of directly dumping them.
    Cache is ordered by named sections. To cache an object, use "cache(object, section_name)".
    All cache sesctions must have been dumped using "dump_cache(section_name)" before the Pickler gets destroyed.
    The output file can be changed at any time using "set_output(file)".
    """

    from .abc import BytesWritable as __BytesWritable



    class __CombinedWriter:

        """
        An internal class to write to multiple file objects as if there was only one.
        """

        def __init__(self) -> None:
            self.__file = None

        @property
        def file(self) -> BytesWritable | None:
            """
            The current output file.
            """
            return self.__file

        def set_file(self, file : BytesWritable):
            """
            Sets the currently active file to write to.
            """
            self.__file = file
        
        def write(self, data : bytes) -> int:
            """
            Writes to the currently active file.
            """
            if self.__file is None:
                raise RuntimeError("No active file in CombinedWriter")
            return self.__file.write(data)
        


    def __init__(self) -> None:
        self.__writer = CachingPickler.__CombinedWriter()
        self.__cache : "dict[str, list[Any]]" = {}
        self.__cache_ids : "dict[str, dict[int, int]]" = {}
        self.__main_dump = True
        super().__init__(self.__writer)

    def cache(self, obj : Any, section_name : str):
        """
        Caches an object to be referenced from outside the cache.
        Objects must be cached before they are pickled or this is useless!
        """
        cache, cache_ids = self.__cache.setdefault(section_name, []), self.__cache_ids.setdefault(section_name, {})
        pid = len(cache)
        cache.append(obj)
        cache_ids[id(obj)] = pid

    def persistent_id(self, obj: Any) -> Any:
        """
        Returns a cache identifier for cached object and None if objects are not in the cache.
        """
        i = id(obj)
        for section_name in self.__cache:
            cache_ids = self.__cache_ids[section_name]
            if i in cache_ids:
                return (section_name, cache_ids[i])

    def set_output(self, file : BytesWritable) -> BytesWritable | None:
        """
        Sets the output file of this Pickler. Returns the previous file.
        """
        if not isinstance(file, CachingPickler.__BytesWritable):
            raise TypeError(f"Expected writable file-like object, got '{type(file).__name__}'")
        old = self.__writer.file
        self.__writer.set_file(file)
        return old
    
    def dump_cache(self, section_name : str):
        """
        Dumps the given cache section if it exists.
        """
        if section_name in self.__cache:
            cache = self.__cache.pop(section_name)
            self.__cache_ids.pop(section_name)
            self.dump((section_name, cache))

    def __contains__(self, obj : Any) -> bool:
        """
        Implements obj in self. Returns True if the object is cached.
        """
        return any(id(obj) in cache_ids for cache_ids in self.__cache_ids.values())
    
    @property
    def cache_sections(self) -> set[str]:
        """
        The set of section names existing in the cache.
        """
        return set(self.__cache)
    
    def __del__(self):
        if self.__cache:
            raise RuntimeError(f"CachingPickler destroyed without dumping all cache: {len(self.__cache)} sections remaining")

    def dump(self, obj: Any) -> None:       # We must overload it so the memo will be reset after the main object has been dumped.
        mine = False
        if self.__main_dump:
            mine = True
            self.__main_dump = False

        super().dump(obj)

        if mine:
            self.__main_dump = True
            self.clear_memo()
    




class CachingUnpickler:

    """
    This subclass of unpickler uses a cache (anything) to reference some objects instead of directly loading them.
    The initial_file argument is used to load the cache.
    The input file can be changed at any time using "set_input(file)".

    Note that it is not directly a subclass of Unpickler, but the "load()" method works identically.
    """

    from .abc import BytesReadable as __BytesReadable



    class __CombinedReader:

        """
        An internal class to read from multiple file objects as if there was only one.
        """

        def __init__(self) -> None:
            self.__file = None

        @property
        def file(self) -> BytesReadable | None:
            """
            The current input file.
            """
            return self.__file

        def set_file(self, file : BytesReadable):
            """
            Sets the currently active file to read from.
            """
            self.__file = file
        
        def read(self, n : int = -1) -> bytes:
            """
            Reads from the currently active file.
            """
            if self.__file is None:
                raise RuntimeError("No active file in CombinedReader")
            return self.__file.read(n)
        
        def readline(self, n : int = -1):
            """
            Reads a line from the file.
            """
            if self.__file is None:
                raise RuntimeError("No active file in CombinedReader")
            return self.__file.readline(n)
        
        def close(self):
            """
            Actually does nothing.
            """
        
    

    class __InternalCachingUnpickler(Unpickler):

        def __init__(self, file : BytesReadable, cache : dict[str, list[Any]]) -> None:
            super().__init__(file)
            self.__cache = cache

        def persistent_load(self, identifier: tuple[str, int]) -> Any:
            section_name, pid = identifier
            if section_name not in self.__cache:
                raise ValueError(f"Unknown cache section: {section_name}")
            cache = self.__cache[section_name]
            if pid >= len(cache):
                raise ValueError(f"Unknown cache pid: {section_name}.{pid}")
            return cache[pid]



    def __init__(self) -> None:
        self.__reader = CachingUnpickler.__CombinedReader()
        self.__cache : "dict[str, list[Any]]" = {}
    
    def set_input(self, file : BytesReadable) -> BytesReadable | None:
        """
        Sets the input file of this Unpickler. Returns the previous file.
        """
        if not isinstance(file, CachingUnpickler.__BytesReadable):
            raise TypeError(f"Expected readable file-like object, got '{type(file).__name__}'")
        old = self.__reader.file
        self.__reader.set_file(file)
        return old
    
    def load_cache(self):
        """
        Loads a part of the cache from the currently active input file.
        """
        try:
            section_name, cache = self.load()
        except:
            raise ValueError("Corrupted cache")
        if not isinstance(section_name, str) or not isinstance(cache, list):
            raise ValueError("Corrupted cache")
        self.__cache.setdefault(section_name, []).extend(cache)
    
    def load(self) -> Any:
        return CachingUnpickler.__InternalCachingUnpickler(self.__reader, self.__cache).load()
    




del Pickler, Unpickler, Any, BytesWritable, BytesReadable