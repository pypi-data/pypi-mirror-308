"""
This module defines a wrapper class for reading and eventually decoding a binary stream.
"""

from typing import Literal, overload

__all__ = ["CodecStream"]





class CodecStream:
    
    """
    A wrapper class for a binary stream. Creates independant and thread safe file-like objects on the underlying stream, which can be used to decode the stream.
    Only allows for reading!
    """

    from codecs import StreamReader as __StreamReader, getreader
    from .sub_file import SectorReader as __SectorReader
    __getreader = staticmethod(getreader)
    del getreader

    def __init__(self, stream : __SectorReader) -> None:
        self.__file = stream

    @overload
    def open(self, mode : Literal["rb"]) -> __SectorReader:
        ...

    @overload
    def open(self, mode : Literal["r", "rt"] = "r", encoding : str | None = None) -> __StreamReader:
        ...

    def open(self, mode : Literal["r", "rb", "rt"] = "r", encoding : str | None = None) -> __SectorReader | __StreamReader:
        """
        Opens a new independent file-like object on the underlying stream, decoding it if opened in text mode (default).
        """
        if not isinstance(mode, str) or (encoding is not None and not isinstance(encoding, str)):
            raise TypeError(f"Expected str, str or None, got '{type(mode).__name__}' and '{type(encoding).__name__}'")
        if mode not in ["r", "rb", "rt"]:
            raise ValueError(f"Supported modes are 'rt' (or 'r') and 'rb', not '{mode}'")
        if mode == "r" or mode == "rt":
            return CodecStream.__getreader(encoding if encoding is not None else "utf-8")(self.open("rb"))
        else:
            return CodecStream.__SectorReader(self.__file, 0, self.__file.size, lock = self.__file.lock)
        




del Literal, overload