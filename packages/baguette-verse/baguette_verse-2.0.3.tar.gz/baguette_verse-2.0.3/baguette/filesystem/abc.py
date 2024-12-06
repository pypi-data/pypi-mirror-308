"""
Just some type chechers utilities for the BAGUETTE file system.
"""

from io import SEEK_SET
from typing import Protocol, runtime_checkable

__all__ = ["BytesReadable", "BytesWritable", "BytesSeekable", "BytesRandom"]





@runtime_checkable
class BytesWritable(Protocol):

    """
    A Protocol class for file-like objects that support writing.
    """

    def write(self, data : bytes, /) -> int:
        raise NotImplementedError
    




@runtime_checkable
class BytesReadable(Protocol):

    """
    A Protocol class for file-like objects that support reading.
    """

    def read(self, n : int = -1, /) -> bytes:
        raise NotImplementedError
    
    def readline(self, n : int = -1, /) -> bytes:
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
    




@runtime_checkable
class BytesSeekable(Protocol):

    """
    A subclass of BytesReadable that also supports seeking and telling.
    """

    def read(self, n : int = -1, /) -> bytes:
        raise NotImplementedError
    
    def readline(self, n : int = -1, /) -> bytes:
        raise NotImplementedError
    
    def seekable(self) -> bool:
        raise NotImplementedError

    def seek(self, offset : int, whence : int = SEEK_SET, /) -> int:
        raise NotImplementedError
    
    def tell(self) -> int:
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
    
    



@runtime_checkable
class BytesRandom(Protocol):


    """
    A Protocol class for file-like objects that support reading, seeking and writing.
    """

    def read(self, n : int = -1, /) -> bytes:
        raise NotImplementedError
    
    def readline(self, n : int = -1, /) -> bytes:
        raise NotImplementedError
    
    def seekable(self) -> bool:
        raise NotImplementedError

    def seek(self, offset : int, whence : int = SEEK_SET, /) -> int:
        raise NotImplementedError
    
    def tell(self) -> int:
        raise NotImplementedError

    def write(self, data : bytes, /) -> int:
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
    
    



del Protocol, runtime_checkable, SEEK_SET