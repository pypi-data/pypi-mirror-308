"""
Defines a class to wrap a temporary file with named sections.
"""

from baguette.filesystem.abc import BytesRandom
from .abc import BytesReadable, BytesWritable
from .sub_file import Sector   

__all__ = ["TMPStorage"]





class TMPStorage:

    """
    Just a class to hold some temporary data into a temporatry file, to retrieve later.
    """

    from io import SEEK_END as __SEEK_END
    from tempfile import TemporaryFile, _TemporaryFileWrapper
    from threading import RLock as __RLock
    __TemporaryFile = staticmethod(TemporaryFile)
    del TemporaryFile, _TemporaryFileWrapper

    COPY_PACKET_SIZE = 2 ** 20

    def __init__(self) -> None:
        self.__file : "TMPStorage._TemporaryFileWrapper[bytes] | None" = None
        self.__index : "dict[str, tuple[int, int]]" = {}
        self.__lock = TMPStorage.__RLock()

    @property
    def index(self) -> dict[str, tuple[int, int]]:
        """
        The index of sectors present in the temporary file.
        """
        with self.__lock:
            return self.__index.copy()
    
    def size(self, name : str) -> int:
        """
        Returns the current size of the sector with the given name.
        """
        with self.__lock:
            return self.__index[name][1] - self.__index[name][0]
    
    class SubReader(Sector):

        from tempfile import _TemporaryFileWrapper
        from threading import RLock

        def __init__(self, temporary_file  : "_TemporaryFileWrapper[bytes]", index : dict[str, tuple[int, int]], name : str, lock : RLock) -> None:
            super().__init__(temporary_file, *index[name])
            self.__lock = lock
        
        def read(self, n: int = -1) -> bytes:
            with self.__lock:
                return super().read(n)
            
        def readline(self, n : int = -1) -> bytes:
            with self.__lock:
                return super().readline(n)
        
        del _TemporaryFileWrapper, RLock

    def file_reader(self, name : str) -> SubReader:
        """
        Returns a file-like object for reading data stored in a sector with the given name of a temporary file.
        """
        with self.__lock:
            if self.__file is None:
                self.__file = TMPStorage.__TemporaryFile("w+b") # type: ignore because "w+b" is not recognized...
            return TMPStorage.SubReader(self.__file, self.__index, name, self.__lock) # type: ignore
    
    def load(self, file : BytesWritable, name : str):
        """
        Transfers the content of the sector with given name into the given file.
        """
        tmp = self.file_reader(name)
        while True:
            data = tmp.read(TMPStorage.COPY_PACKET_SIZE)
            if not data:
                break
            file.write(data)
    
    class SubWriter(Sector):

        from io import SEEK_CUR as __SEEK_CUR, SEEK_END as __SEEK_END, SEEK_SET as __SEEK_SET
        from tempfile import _TemporaryFileWrapper
        from threading import RLock

        def __init__(self, temporary_file : "_TemporaryFileWrapper[bytes]", index : dict[str, tuple[int, int]], name : str, lock : RLock) -> None:
            if name in index:
                for sname, (start, stop) in index.items():
                    if sname != name and stop > index[name][1]:
                        raise RuntimeError("Cannot write in a sector that is not the last one")
            lock.acquire()
            self.__file = temporary_file
            end = temporary_file.seek(0, TMPStorage.SubWriter.__SEEK_END)
            index.setdefault(name, (end, end))[0]
            super().__init__(temporary_file, index[name][0])
            self.__index = index
            self.__name = name
            self.__lock = lock
        
        def seek(self, offset: int = 0, whence: int = __SEEK_SET):
            return super().seek(offset, whence)

        def write(self, data: bytes) -> int:
            n = super().write(data)
            self.__index[self.__name] = (self.__index[self.__name][0], max(self.__index[self.__name][1], self.__file.tell()))
            return n
            
        def __del__(self):
            self.__lock.release()
        
        del _TemporaryFileWrapper, RLock

    def file_writer(self, name : str) -> SubWriter:
        """
        Returns a file-like object for writing data into a new sector with the given name of a temporary file.
        """
        with self.__lock:
            if self.__file is None:
                self.__file = TMPStorage.__TemporaryFile("w+b") # type: ignore because "w+b" is not recognized...
            return TMPStorage.SubWriter(self.__file, self.__index, name, self.__lock) # type: ignore
    
    def save(self, file : BytesReadable, name : str, n : int | float = float("inf")):
        """
        Transfers at most n bytes of file into a sector of a temporary file with given name.
        """
        tmp = self.file_writer(name)
        tmp.seek(0, TMPStorage.__SEEK_END)
        i = 0
        while i < n:
            data = file.read(min(TMPStorage.COPY_PACKET_SIZE, n - i)) # type: ignore because float("inf") may not be the minimum
            if not data:
                break
            i += tmp.write(data)