"""
This module adds new classes of file-like objects that allow reading from another file but in a limited range as if it was a whole file. 
"""

from .abc import BytesSeekable, BytesRandom

__all__ = ["SectorReader", "Sector"]





class SectorReader[Stream : BytesSeekable](BytesSeekable):

    """
    A file-like object that reads from a limited section of a file. They are thread-safe.
    """

    from io import SEEK_SET as __SEEK_SET, SEEK_CUR as __SEEK_CUR, SEEK_END as __SEEK_END
    from threading import RLock
    __RLock = staticmethod(RLock)

    def __init__(self, file : Stream, min_offset : int, max_offset : int | None = None, *, lock : "RLock | None" = None) -> None:
        self.__file = file
        self.__min = min_offset
        self.__max = max_offset
        self.__pos = min_offset
        self.__lock = SectorReader.__RLock() if lock is None else lock
        self.__closed = False

    @property
    def stream(self) -> Stream:
        """
        The underlying stream. Avoid using it if you just received a SectorReader from a function.
        """
        return self.__file

    @property
    def lock(self) -> RLock:
        """
        The reentrant lock used for making operations thread-safe.
        """
        return self.__lock
    
    @property
    def size(self) -> int | None:
        """
        Returns the maximum offset that can be seeked to in this SectorReader. None if no limit.
        """
        return self.__max - self.__min if self.__max is not None else None

    def read(self, n: int = -1) -> bytes:
        with self.__lock:
            if self.__closed:
                raise IOError("SectorReader is closed")
            self.__file.seek(self.__pos)
            if self.__max is not None:
                if n == -1:
                    n = self.__max - self.__pos
                n = min(n, self.__max - self.__pos)
            data = self.__file.read(n)
            self.__pos += len(data)
            return data
    
    def readline(self, n: int = -1) -> bytes:
        with self.__lock:
            if self.__closed:
                raise IOError("SectorReader is closed")
            self.__file.seek(self.__pos)
            if self.__max is not None:
                if n == -1:
                    n = self.__max - self.__pos
                n = min(n, self.__max - self.__pos)
            data = self.__file.readline(n)
            self.__pos += len(data)
            return data
    
    def seekable(self) -> bool:
        return True
    
    def seek(self, offset: int = 0, whence: int = __SEEK_SET):
        with self.__lock:
            if self.__closed:
                raise IOError("SectorReader is closed")
            match whence:
                case SectorReader.__SEEK_SET:
                    self.__pos = self.__min + offset
                case SectorReader.__SEEK_CUR:
                    self.__pos += offset
                case SectorReader.__SEEK_END:
                    self.__pos = self.__max + offset if self.__max is not None else self.__file.seek(0, SectorReader.__SEEK_END) + offset
            return self.__pos - self.__min
    
    def tell(self) -> int:
        with self.__lock:
            if self.__closed:
                raise IOError("SectorReader is closed")
            return self.__pos - self.__min
        
    def close(self):
        with self.__lock:
            self.__closed = True
    
    del RLock





class Sector[Stream : BytesRandom](BytesRandom):

    """
    A file-like object that reads from and writes to a limited section of a file.
    """

    from io import SEEK_SET as __SEEK_SET, SEEK_CUR as __SEEK_CUR, SEEK_END as __SEEK_END
    from threading import RLock
    __RLock = staticmethod(RLock)

    def __init__(self, file : Stream, min_offset : int, max_offset : int | None = None, *, lock : "RLock | None" = None) -> None:
        self.__file = file
        self.__min = min_offset
        self.__max = max_offset
        self.__pos = min_offset
        self.__lock = Sector.__RLock() if lock is None else lock
        self.__closed = False

    @property
    def stream(self) -> Stream:
        """
        The underlying stream. Avoid using it if you just received a Sector from a function.
        """
        return self.__file
    
    @property
    def window(self) -> slice:
        """
        The accessible range in the underlying buffer (in its remote coordinates). Avoid using it if you just received a Sector from a function.
        """
        return slice(self.__min, self.__max)
    
    @property
    def lock(self) -> RLock:
        """
        The reentrant lock used for making operations thread-safe.
        """
        return self.__lock
    
    @property
    def size(self) -> int | None:
        """
        Returns the maximum offset that can be seeked to in this Sector. None if no limit.
        """
        return self.__max - self.__min if self.__max is not None else None

    def read(self, n: int = -1) -> bytes:
        with self.__lock:
            if self.__closed:
                raise IOError("SectorReader is closed")
            self.__file.seek(self.__pos)
            if self.__max is not None:
                if n == -1:
                    n = self.__max - self.__pos
                n = min(n, self.__max - self.__pos)
            data = self.__file.read(n)
            self.__pos += len(data)
            return data
    
    def readline(self, n: int = -1) -> bytes:
        with self.__lock:
            if self.__closed:
                raise IOError("SectorReader is closed")
            self.__file.seek(self.__pos)
            if self.__max is not None:
                if n == -1:
                    n = self.__max - self.__pos
                n = min(n, self.__max - self.__pos)
            data = self.__file.readline(n)
            self.__pos += len(data)
            return data
    
    def seekable(self) -> bool:
        return True
    
    def seek(self, offset: int = 0, whence: int = __SEEK_SET):
        with self.__lock:
            if self.__closed:
                raise IOError("SectorReader is closed")
            match whence:
                case Sector.__SEEK_SET:
                    self.__pos = self.__min + offset
                case Sector.__SEEK_CUR:
                    self.__pos += offset
                case Sector.__SEEK_END:
                    self.__pos = self.__max + offset if self.__max is not None else self.__file.seek(0, Sector.__SEEK_END) + offset
            return self.__pos - self.__min
    
    def tell(self) -> int:
        return self.__pos - self.__min
    
    def write(self, data : bytes) -> int:
        with self.__lock:
            if self.__closed:
                raise IOError("SectorReader is closed")
            self.__file.seek(self.__pos)
            data = memoryview(data)
            if self.__max is not None and len(data) > self.__max - self.__pos:
                data = data[:self.__max - self.__pos]
            n = self.__file.write(data)
            self.__pos += n
            return n
    
    def close(self):
        with self.__lock:
            self.__closed = True
    
    del RLock





del BytesSeekable, BytesRandom