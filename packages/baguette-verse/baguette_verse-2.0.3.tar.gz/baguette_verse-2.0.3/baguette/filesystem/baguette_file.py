"""
This module defines the BaguetteFile format (.bag) and a class with methods to work with them.

It defines the ".bag" file format:
    - A shebang to a python interpreter and the script to load BaguetteFiles for Unix platforms
    - The JSON data containing the BAGUETTE metadata (compilation and pattern extraction parameters)
    - The input report itself
    - The BAGUETTE Graph
    - The MetaGraphs patterns to search in the BAGUETTE Graph.
    - The extracted MetaGraph Matches if any.
"""

from pathlib import Path
from types import TracebackType
from typing import Any, BinaryIO, Callable, Iterable, Literal, Self, overload
from traceback import TracebackException

from baguette.filesystem.metadata import MetadataContextManager

from ..exit_codes import ExitCode
from ..bakery.source.filters import Filter

__all__ = ["BaguetteFile", "BaguetteFormatError", "is_baguette_file"]





class BaguetteFormatError(Exception):

    """
    This class of Exception indicates that a BaguetteFile has a format error, is corrupted or has some missing information.
    """

    from json import dumps
    from .metadata import BaguetteMetadata
    __dumps = staticmethod(dumps)
    del dumps

    def __init__(self, message : str, file : Path, metadata : BaguetteMetadata) -> None:
        super().__init__(message)
        self.add_note(f"BaguetteFile: '{file}'")
        if metadata is not None:
            try:
                self.add_note(f"BAGUETTE metadata:\n{BaguetteFormatError.__dumps(metadata)}")
            except:
                self.add_note(f"BAGUETTE metadata: {metadata}")
        self.file = file
        self.metadata = metadata

    del BaguetteMetadata

ExitCode.register_error_code_checker(ExitCode.BAGUETTE_FORMAT_ERROR, lambda exc, **kwargs : isinstance(exc, BaguetteFormatError))





class BaguetteFile:

    """
    This class allows for reading an writing BaguetteFiles (.bag) at a given path.
    Opening mode can be set to:
        - "r" for readonly mode. The BaguetteFile must exist.
        - "r+" for read and write mode. The BaguetteFile must exist.
        - "w" for erasing if it exists then reading and writing.
        - "x" for creating then reading and writing. The BaguetteFile must not exist.
        - None (default) for creating if it does not exist, then reading and writing.
    """

    from bz2 import BZ2File as __BZ2File
    from collections.abc import Buffer as __Buffer
    from io import SEEK_END as __SEEK_END
    from inspect import BufferFlags as __BufferFlags
    from json import loads as __jloads__, dumps as __jdumps__
    from pathlib import Path as __Path
    from traceback import TracebackException as __TracebackException
    from typing import Iterable as __Iterable
    from stat import S_IEXEC as __S_IEXEC
    from sys import platform as __platform
    from weakref import ref as __ref
    from ..bakery.source.colors import Color as __Color
    from ..bakery.source.graph import Edge as __Edge, Vertex as __Vertex, FrozenGraph as __FrozenGraph, Graph as __Graph
    from .abc import BytesReadable as __BytesReadable, BytesSeekable as __BytesSeekable
    from .binary_decoder import CodecStream as __CodecStream
    from .data import Data as __Data
    from .tmp_file_storage import TMPStorage as __TMPStorage
    from .caching_pickle import CachingPickler as __CachingPickler, CachingUnpickler as __CachingUnpickler
    from .match_file_iterator import MatchFileSequence as __MatchFileSequence
    from .sub_file import SectorReader as __SectorReader, Sector as __Sector
    from .metadata import BaguetteMetadata as __BaguetteMetadata
    from ..croutons.source.metagraph import FrozenMetaGraph as __FrozenMetaGraph, MetaGraph as __MetaGraph
    __jloads = staticmethod(__jloads__)
    __jdumps = staticmethod(__jdumps__)
    del __jdumps__, __jloads__



    class UpdateContext(MetadataContextManager):

        def __init__(self, enter_func : Callable[[], None], exit_func : Callable[[], None]) -> None:
            self.__level = 0
            self.__enter_func = enter_func
            self.__exit_func = exit_func
            self.__enabled = True

        def disable(self):
            self.__enabled = False

        def enable(self):
            self.__enabled = True

        def __enter__(self):
            if not self.__level and self.__enabled:
                self.__enter_func()
            self.__level += 1
        
        def __exit__[E : BaseException](self, exc_type : type[E] | None = None, exc : E | None = None, traceback : TracebackType | None = None):
            self.__level -= 1
            if not self.__level and self.__enabled:
                self.__exit_func()

    

    UNIX_EXEC_SCRIPT = (Path(__file__).parent.parent / "setup" / "unix_open.sh").read_text()
    BAGUETTE_HEADER = "  🥖   🥖🥖  🥖      🥖    🥖  🥖🥖    🥖 🥖🥖  🥖🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖  🥖 🥖 🥖🥖🥖 🥖   🥖🥖🥖 🥖   🥖🥖  🥖 🥖  🥖      🥖 🥖  🥖  🥖🥖  🥖 🥖 🥖🥖   🥖🥖 🥖🥖 🥖  🥖 🥖🥖🥖     🥖🥖  🥖 🥖  🥖     🥖🥖🥖🥖    🥖  🥖🥖🥖🥖🥖🥖 🥖  🥖 🥖🥖  🥖 🥖🥖     🥖🥖 🥖    🥖 🥖   🥖   🥖🥖  🥖   🥖🥖  🥖      🥖  🥖  🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖🥖🥖 🥖🥖🥖  🥖  🥖🥖  🥖 🥖 🥖🥖  🥖   🥖🥖 🥖  🥖 🥖🥖  🥖 🥖 🥖🥖 🥖🥖🥖  🥖🥖🥖 🥖   🥖🥖🥖  🥖🥖  🥖🥖🥖 🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖       🥖🥖   🥖 🥖  🥖 🥖🥖 🥖🥖  🥖🥖🥖  🥖      🥖 🥖 🥖    🥖🥖 🥖🥖   🥖🥖 🥖 🥖  🥖      🥖🥖  🥖🥖  🥖🥖 🥖🥖   🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖🥖  🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖       🥖🥖 🥖🥖🥖  🥖🥖      🥖🥖     🥖🥖  🥖🥖🥖  🥖      🥖🥖🥖 🥖🥖🥖 🥖🥖    🥖 🥖🥖🥖 🥖   🥖🥖  🥖 🥖 🥖🥖🥖  🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖       🥖🥖🥖    🥖🥖  🥖🥖🥖  🥖      🥖🥖  🥖   🥖🥖🥖  🥖  🥖🥖🥖🥖  🥖  🥖      🥖🥖   🥖  🥖🥖    🥖 🥖🥖 🥖 🥖🥖 🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖🥖🥖  🥖      🥖🥖🥖🥖  🥖 🥖🥖  🥖 🥖 🥖🥖    🥖 🥖🥖🥖  🥖🥖 🥖🥖🥖 🥖      🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖       🥖🥖  🥖   🥖🥖  🥖  🥖🥖  🥖🥖🥖  🥖      🥖🥖🥖  🥖🥖 🥖🥖    🥖 🥖🥖 🥖🥖   🥖🥖🥖 🥖      🥖🥖 🥖    🥖 🥖   🥖   🥖🥖  🥖   🥖🥖  🥖      🥖 🥖     🥖🥖🥖  🥖  🥖🥖  🥖 🥖 🥖🥖🥖     🥖🥖    🥖 🥖🥖🥖  🥖  🥖🥖    🥖 🥖🥖🥖 🥖   🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖🥖 🥖🥖 🥖🥖🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖      🥖  🥖🥖 🥖 🥖🥖 🥖  🥖 🥖🥖🥖🥖     🥖      🥖🥖    🥖 🥖🥖 🥖🥖   🥖🥖 🥖🥖    🥖      🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖🥖🥖 🥖🥖🥖  🥖  🥖🥖  🥖 🥖 🥖🥖  🥖   🥖🥖 🥖  🥖 🥖🥖  🥖 🥖 🥖🥖 🥖🥖🥖  🥖🥖🥖 🥖   🥖🥖🥖  🥖🥖  🥖 🥖🥖    🥖      🥖🥖🥖🥖  🥖 🥖🥖  🥖 🥖 🥖🥖    🥖 🥖🥖🥖  🥖🥖 🥖🥖🥖 🥖    🥖      🥖🥖 🥖🥖   🥖🥖    🥖 🥖🥖🥖  🥖🥖 🥖🥖🥖 🥖    🥖 🥖🥖    🥖      🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖   🥖      🥖🥖    🥖  🥖      🥖🥖   🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖🥖🥖 🥖🥖 🥖🥖    🥖      🥖🥖    🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖    🥖      🥖🥖 🥖🥖   🥖🥖  🥖 🥖 🥖🥖🥖 🥖    🥖      🥖🥖 🥖  🥖 🥖🥖🥖 🥖    🥖      🥖🥖🥖  🥖🥖 🥖🥖 🥖  🥖 🥖🥖🥖 🥖    🥖      🥖🥖  🥖🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖  🥖   🥖       🥖🥖  🥖   🥖🥖      🥖      🥖🥖 🥖🥖 🥖 🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖  🥖🥖🥖 🥖 🥖 🥖🥖🥖 🥖   🥖🥖  🥖 🥖 🥖🥖🥖  🥖🥖  🥖 🥖🥖🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖      🥖 🥖  🥖🥖 🥖🥖🥖 🥖   🥖🥖🥖  🥖  🥖🥖  🥖 🥖 🥖🥖🥖 🥖   🥖🥖   🥖🥖 🥖🥖 🥖     🥖 🥖🥖    🥖      🥖🥖  🥖🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖 🥖🥖   🥖🥖  🥖    🥖      🥖🥖    🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖    🥖      🥖🥖 🥖🥖   🥖🥖  🥖 🥖 🥖🥖🥖 🥖    🥖      🥖🥖🥖  🥖🥖 🥖🥖 🥖  🥖 🥖🥖🥖 🥖    🥖      🥖🥖  🥖🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖  🥖   🥖       🥖🥖  🥖🥖  🥖🥖      🥖      🥖🥖 🥖🥖 🥖 🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖  🥖🥖🥖 🥖 🥖 🥖🥖🥖 🥖   🥖🥖  🥖 🥖 🥖🥖🥖  🥖🥖  🥖 🥖🥖🥖   🥖      🥖 🥖  🥖  🥖🥖  🥖 🥖 🥖🥖🥖     🥖🥖  🥖 🥖 🥖🥖    🥖 🥖🥖🥖 🥖    🥖       🥖🥖  🥖🥖  🥖      🥖🥖🥖 🥖   🥖🥖 🥖  🥖 🥖🥖 🥖🥖 🥖 🥖🥖  🥖 🥖 🥖🥖🥖  🥖🥖  🥖 🥖🥖🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖      🥖    🥖🥖 🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖🥖  🥖🥖  🥖 🥖 🥖🥖🥖  🥖   🥖      🥖🥖🥖 🥖   🥖🥖 🥖    🥖🥖  🥖 🥖  🥖      🥖🥖   🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖🥖🥖 🥖🥖 🥖🥖    🥖      🥖🥖🥖 🥖🥖🥖 🥖🥖 🥖  🥖 🥖🥖🥖 🥖   🥖🥖 🥖     🥖      🥖🥖🥖     🥖🥖 🥖🥖   🥖🥖    🥖 🥖🥖🥖  🥖🥖 🥖🥖🥖 🥖   🥖🥖 🥖  🥖 🥖🥖   🥖🥖  🥖      🥖🥖🥖 🥖🥖🥖 🥖🥖🥖  🥖  🥖🥖    🥖 🥖🥖🥖      🥖      🥖🥖    🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖    🥖      🥖🥖🥖     🥖🥖 🥖🥖   🥖🥖    🥖 🥖🥖   🥖🥖 🥖🥖  🥖 🥖  🥖      🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖   🥖      🥖🥖🥖 🥖   🥖🥖 🥖    🥖🥖  🥖 🥖  🥖      🥖🥖  🥖🥖  🥖🥖🥖  🥖  🥖🥖 🥖  🥖 🥖🥖  🥖   🥖🥖  🥖🥖🥖 🥖🥖  🥖 🥖  🥖      🥖🥖  🥖🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖  🥖   🥖       🥖🥖   🥖  🥖🥖  🥖   🥖      🥖🥖 🥖    🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖🥖  🥖  🥖🥖🥖  🥖🥖  🥖 🥖🥖🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖      🥖 🥖 🥖   🥖🥖    🥖 🥖🥖 🥖 🥖🥖 🥖🥖  🥖 🥖  🥖      🥖🥖🥖 🥖   🥖🥖 🥖    🥖🥖  🥖 🥖  🥖      🥖🥖  🥖   🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖  🥖🥖🥖 🥖🥖 🥖     🥖      🥖🥖   🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖🥖🥖 🥖🥖 🥖🥖    🥖      🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖🥖 🥖    🥖      🥖🥖    🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖    🥖      🥖🥖🥖     🥖🥖🥖  🥖  🥖🥖  🥖 🥖 🥖🥖 🥖    🥖🥖  🥖 🥖 🥖🥖    🥖 🥖🥖🥖 🥖    🥖      🥖🥖🥖 🥖   🥖🥖 🥖    🥖🥖  🥖 🥖  🥖      🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖🥖  🥖🥖  🥖 🥖 🥖🥖 🥖🥖🥖   🥖      🥖🥖    🥖 🥖🥖🥖 🥖    🥖       🥖🥖  🥖   🥖🥖 🥖 🥖  🥖🥖    🥖🥖    🥖 🥖 🥖     🥖🥖    🥖 🥖 🥖🥖     🥖    🥖🥖  🥖      🥖🥖🥖 🥖🥖🥖 🥖🥖 🥖  🥖 🥖🥖🥖 🥖   🥖🥖 🥖     🥖      🥖🥖    🥖  🥖      🥖🥖   🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖🥖🥖 🥖🥖 🥖🥖    🥖      🥖🥖 🥖🥖🥖🥖 🥖🥖  🥖🥖   🥖      🥖🥖🥖 🥖🥖🥖 🥖🥖    🥖 🥖🥖🥖 🥖   🥖🥖  🥖 🥖 🥖🥖🥖  🥖   🥖 🥖🥖🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖      🥖    🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖🥖 🥖    🥖      🥖🥖🥖 🥖   🥖🥖 🥖    🥖🥖  🥖 🥖  🥖      🥖🥖   🥖  🥖🥖    🥖 🥖🥖  🥖🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖  🥖 🥖 🥖🥖🥖 🥖   🥖🥖🥖 🥖   🥖🥖  🥖 🥖  🥖      🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖  🥖🥖🥖 🥖   🥖🥖 🥖🥖🥖🥖  🥖      🥖🥖🥖  🥖🥖 🥖🥖 🥖    🥖🥖    🥖 🥖🥖🥖     🥖🥖  🥖 🥖  🥖      🥖🥖🥖 🥖🥖🥖 🥖🥖 🥖  🥖 🥖🥖🥖 🥖   🥖🥖 🥖     🥖      🥖🥖    🥖  🥖      🥖🥖 🥖 🥖🥖 🥖🥖 🥖🥖🥖  🥖🥖 🥖  🥖 🥖🥖  🥖🥖  🥖🥖  🥖 🥖  🥖 🥖🥖🥖     🥖🥖 🥖    🥖 🥖   🥖 🥖🥖 🥖  🥖      🥖    🥖  🥖🥖    🥖 🥖🥖 🥖 🥖🥖 🥖🥖  🥖 🥖  🥖      🥖🥖  🥖🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖  🥖   🥖      🥖🥖    🥖 🥖🥖🥖  🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖    🥖       🥖🥖   🥖  🥖🥖 🥖 🥖  🥖      🥖🥖 🥖🥖 🥖 🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖  🥖🥖🥖 🥖 🥖 🥖🥖🥖 🥖   🥖🥖  🥖 🥖 🥖🥖🥖  🥖🥖  🥖       🥖 🥖    🥖🥖 🥖🥖 🥖 🥖🥖 🥖🥖🥖🥖 🥖🥖🥖  🥖  🥖🥖  🥖 🥖  🥖      🥖🥖 🥖🥖🥖🥖 🥖🥖🥖  🥖   🥖      🥖🥖 🥖🥖   🥖🥖  🥖 🥖 🥖🥖🥖  🥖🥖 🥖🥖🥖  🥖🥖  🥖      🥖🥖🥖 🥖   🥖🥖 🥖🥖🥖🥖  🥖      🥖🥖🥖🥖  🥖 🥖🥖 🥖🥖🥖🥖 🥖🥖🥖 🥖 🥖 🥖🥖🥖  🥖   🥖      🥖🥖 🥖🥖   🥖🥖 🥖  🥖 🥖🥖 🥖 🥖🥖 🥖🥖 🥖  🥖 🥖🥖 🥖🥖🥖  🥖🥖  🥖🥖🥖  🥖 🥖  🥖  🥖 🥖🥖🥖     🥖🥖 🥖    🥖 🥖   🥖   🥖🥖  🥖   🥖🥖  🥖      🥖   🥖 🥖 🥖🥖 🥖🥖🥖  🥖🥖 🥖 🥖  🥖🥖 🥖🥖🥖🥖 🥖🥖🥖🥖  🥖  🥖     🥖🥖🥖🥖    🥖  🥖🥖🥖🥖🥖🥖 🥖  🥖 🥖🥖  🥖 🥖🥖 🥖🥖🥖🥖    🥖  🥖🥖🥖🥖🥖🥖   🥖🥖 🥖🥖 🥖🥖 🥖🥖🥖🥖🥖🥖🥖    🥖  🥖🥖🥖🥖🥖🥖    🥖🥖🥖🥖 🥖 🥖 🥖🥖🥖🥖🥖🥖    🥖  🥖🥖🥖🥖🥖🥖    🥖🥖🥖🥖 🥖🥖 🥖🥖🥖"
    COPY_PACKET_SIZE = 2 ** 20
    POINTER_BYTE_SIZE = 8




    @staticmethod
    def is_baguette_file(path : __Path | str) -> bool:
        """
        Returns True if the file at given path exists, is a file and is a BAGUETTE file.
        """
        if isinstance(path, str):
            path = BaguetteFile.__Path(path)
        if not isinstance(path, BaguetteFile.__Path):
            raise TypeError(f"Expected Path or str, got '{type(path).__name__}'")
        if not path.is_file():
            return False
        with path.open("rb") as f:
            for line in f:
                if line.endswith(BaguetteFile.BAGUETTE_HEADER.encode() + b"\n"):
                    return True
            else:
                return False

    def __init__(self, path : __Path | str, *, mode : Literal["r", "x", "w", "r+"] | None = None) -> None:
        if isinstance(path, str):
            path = BaguetteFile.__Path(path)
        if not isinstance(path, BaguetteFile.__Path):
            raise TypeError(f"Expected Path object, got '{type(path).__name__}'")
        if mode is not None and not isinstance(mode, str):
            raise TypeError(f"Expected str or None for mode, got '{type(mode).__name__}'")
        if path.exists() and path.is_dir():
            raise FileExistsError(f"Given path exists and is not a file : '{path}'\nMaybe it is an old version of BAGUETTE?")
        if mode is None:
            mode = "r+" if path.exists() else "w"

        self.__path = path
        self.__readonly = mode == "r"
        self.__closed = False
        self.__disk_references = 0

        match mode:
            case "r":
                filemode = "rb"
            case "r+":
                filemode = "r+b"
            case "w":
                filemode = "w+b"
            case "x":
                filemode = "x+b"
        self.__filemode : 'Literal["rb", "r+b", "w+b", "x+b"]' = filemode

        self.__fd = None
        self.__data_fd = None
        # self.__fd = path.open(filemode)

        self.__last_change = -float("inf")

        self.__report = None
        self.__baguette : "None | BaguetteFile.__FrozenGraph" = None
        self.__patterns : "None | frozenset[BaguetteFile.__FrozenMetaGraph]" = None
        self.__matches : "None | BaguetteFile.__MatchFileSequence" = None
        self.__dict : "None | BaguetteFile.__Data" = None

        self.__unpickler = None
        self.__pickler = None

        self.__filtered_baguette = None

        self.__report_offset = -1
        self.__report_size = 0
        self.__graph_cache_offset = -1
        self.__graph_cache_size = 0
        self.__baguette_offset = -1
        self.__baguette_size = 0
        self.__patterns_offset = -1
        self.__patterns_size = 0
        self.__meta_cache_offset = -1
        self.__meta_cache_size = 0
        self.__matches_offset = -1
        self.__matches_size = 0
        self.__dict_offset = -1
        self.__dict_size = 0

        def enter():
            if self.__readonly:
                raise ValueError("BaguetteFile opened in read-only mode")
        def exit():
            self.__modified_metadata = True

        self.__modified_metadata = False
        self.__modified_metadata_context_manager = BaguetteFile.UpdateContext(enter, exit)

        self.__disk_metadata_size = 0
        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        if not self.readonly:
            self.__increase_disk_reference_count()
        self.__decrease_disk_reference_count()

    @property
    def metadata(self) -> __BaguetteMetadata:
        """
        The metadata of the BaguetteFile.
        """
        return self.__metadata
    
    @property
    def closed(self) -> bool:
        """
        True if the file is still opened.
        """
        return self.__closed
    
    def close(self):
        """
        Closes the BaguetteFile.
        """
        self.save_metadata()
        if not self.readonly and not self.__closed:
            self.__decrease_disk_reference_count()
            self.__closed = True
    
    # MAKE SURE TO KEEP THE SAME POINTER ORDERS BETWEEN __get_pointers() et __set_pointers()
    
    @overload
    def __get_pointers(self, name : Literal["report", "graph_cache", "baguette", "patterns", "meta_cache", "matches", "dict"]) -> tuple[int, int]:
        pass

    @overload
    def __get_pointers(self) -> tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int]:
        pass

    def __get_pointers(self, name : Literal["report", "graph_cache", "baguette", "patterns", "meta_cache", "matches", "dict"] | None = None):
        """
        Without argument, returns the pointers in fixed order to the different sections in the BaguetteFile.
        With a section name, returns the position ans size of the given section.
        """
        if name is None:
            return (
                self.__report_offset, self.__report_size,
                self.__graph_cache_offset, self.__graph_cache_size,
                self.__baguette_offset, self.__baguette_size,
                self.__meta_cache_offset, self.__meta_cache_size,
                self.__patterns_offset, self.__patterns_size,
                self.__matches_offset, self.__matches_size,
                self.__dict_offset, self.__dict_size
            )
        else:
            match name:
                case "report":
                    return self.__report_offset, self.__report_size
                case "graph_cache":
                    return self.__graph_cache_offset, self.__graph_cache_size
                case "baguette":
                    return self.__baguette_offset, self.__baguette_size
                case "meta_cache":
                    return self.__meta_cache_offset, self.__meta_cache_size
                case "patterns":
                    return self.__patterns_offset, self.__patterns_size
                case "matches":
                    return self.__matches_offset, self.__matches_size
                case "dict":
                    return self.__dict_offset, self.__dict_size
    
    def __set_pointers(self,
                       report_offset : int | None = None,
                       report_size : int | None = None,
                       graph_cache_offset : int | None = None,
                       graph_cache_size : int | None = None,
                       baguette_offset : int | None = None,
                       baguette_size : int | None = None,
                       meta_cache_offset : int | None = None,
                       meta_cache_size : int | None = None,
                       patterns_offset : int | None = None,
                       patterns_size : int | None = None,
                       matches_offset : int | None = None,
                       matches_size : int | None = None,
                       dict_offset : int | None = None,
                       dict_size : int | None = None):
        """
        Sets all the pointers in the BaguetteFile object at once.
        """
        with self.__modified_metadata_context_manager:
            if report_offset is not None:
                self.__report_offset = report_offset
            if report_size is not None:
                self.__report_size = report_size
            if graph_cache_offset is not None:
                self.__graph_cache_offset = graph_cache_offset
            if graph_cache_size is not None:
                self.__graph_cache_size = graph_cache_size
            if baguette_offset is not None:
                self.__baguette_offset = baguette_offset
            if baguette_size is not None:
                self.__baguette_size = baguette_size
            if meta_cache_offset is not None:
                self.__meta_cache_offset = meta_cache_offset
            if meta_cache_size is not None:
                self.__meta_cache_size = meta_cache_size
            if patterns_offset is not None:
                self.__patterns_offset = patterns_offset
            if patterns_size is not None:
                self.__patterns_size = patterns_size
            if matches_offset is not None:
                self.__matches_offset = matches_offset
            if matches_size is not None:
                self.__matches_size = matches_size
            if dict_offset is not None:
                self.__dict_offset = dict_offset
            if dict_size is not None:
                self.__dict_size = dict_size

    def __increase_disk_reference_count(self) -> tuple[BinaryIO, __Sector[BinaryIO]]:
        """
        Internal function used to increase the number of references to disk data.
        """
        self.__disk_references += 1

        if self.__fd is None or self.__data_fd is None:
            if self.__disk_references > 1:
                raise RuntimeError("File descriptors did not exist with nonzero disk reference count")
            if self.__filemode in ("rb", "r+b") and not self.__path.exists():
                raise FileNotFoundError(f"BaguetteFile not found when opening in read-only mode: '{self.__path}'")
            if self.__path.exists() and self.__filemode == "x+b":
                raise FileExistsError(f"BaguetteFile already exists in exclusive creation mode: '{self.__path}'")
            existed = self.__path.exists()
            self.__fd = self.__path.open(self.__filemode)
            if not self.__readonly and not existed:
                self.__data_fd = self.__touch_baguette_file(self.__fd)
            else:
                if self.__check_file_changed():
                    self.__data_fd = self.__load_metadata(self.__fd)
                else:
                    self.__data_fd = BaguetteFile.__Sector(self.__fd, self.__disk_metadata_size)

        return self.__fd, self.__data_fd

    def __decrease_disk_reference_count(self):
        """
        Internal function used to decrease the number of references to disk data.
        Closes the opened file if it reaches zero.
        """
        self.__disk_references -= 1
        if self.__disk_references < 0:
            raise RuntimeError("Disk reference count got negative.")
        elif not self.__disk_references:
            self.__mark_file_unchanged()
            if self.__fd:
                self.__fd.close()
                self.__fd = None
            self.__data_fd = None

    def __touch_baguette_file(self, file : BinaryIO) -> __Sector[BinaryIO]:
        """
        Internal function used to create the BaguetteFile on disk if it does not exist.
        """
        if self.__readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if BaguetteFile.__platform != "win32":
            st = self.__path.stat()
            self.__path.chmod(st.st_mode | BaguetteFile.__S_IEXEC)
        self.__metadata = self.__default_metadata
        return self.__write_metadata(file)

    def __check_file_changed(self) -> bool:
        """
        Internal function to check that the BaguetteFile has not changed on disk since the last reading.
        Returns True if the file has changed.
        """
        if not self.__path.exists():
            return True
        if self.__path.stat().st_mtime_ns > self.__last_change:
            return True
        return False
    
    def __reload_metatada_on_change(self):
        """
        Internal function to reload the metadata from disk if the file has changed.
        """
        if self.__check_file_changed():
            self.__fd, self.__data_fd = self.__increase_disk_reference_count()
            self.__decrease_disk_reference_count()
    
    def __mark_file_unchanged(self):
        """
        Internal function used to signal that the current version of the file is the one on disk.
        """
        if not self.__path.exists():
            raise FileNotFoundError(f"BaguetteFile does not exist: '{self.__path}'")
        self.__last_change = self.__path.stat().st_mtime_ns

    def __load_metadata(self, file : BinaryIO) -> __Sector[BinaryIO]:
        """
        Internal function that loads the metadata of the given file.
        Returns the data sector.
        """
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        self.__modified_metadata_context_manager.disable()
        self.__metadata : "BaguetteFile.__BaguetteMetadata" = self.__default_metadata
        file.seek(0)
        try:
            line = b""
            while not line.endswith(BaguetteFile.BAGUETTE_HEADER.encode() + b"\n"):
                line = file.readline()
                if not line:
                    return self.__write_metadata(file)
            first_line = file.readline()
            if first_line != b"{\n":
                return self.__write_metadata(file)
            raw_data = [first_line]
            for line in file:
                raw_data.append(line)
                if line == b"}\n":
                    break
            self.__set_pointers(*(int.from_bytes(file.read(BaguetteFile.POINTER_BYTE_SIZE), "little", signed = True) for _ in self.__get_pointers()))
            new_data = BaguetteFile.__jloads(b"".join(raw_data))
            self.__data_fd = BaguetteFile.__Sector(file, file.tell())
            self.__disk_metadata_size = file.tell()
            if self.__modified_metadata:
                raise RuntimeError("Metadata modifications diverge on disk and locally.")
            self.__metadata.import_dict(new_data)
            return self.__data_fd
        except BaseException as e:
            return self.__write_metadata(file)
        finally:
            self.__modified_metadata_context_manager.enable()

    def save_metadata(self):
        """
        Use this function to save the metadata of the BaguetteFile to disk. Called automatically at destruction.
        """
        if self.__modified_metadata:
            self.__fd, self.__data_fd = self.__increase_disk_reference_count()
            try:
                self.__rewrite_metadata()
            finally:
                self.__decrease_disk_reference_count()

    def __del__(self):
        self.close()

    @property
    def __default_metadata(self) -> __BaguetteMetadata:
        """
        Internal function that returns the default metadata of BaguetteFiles.
        """
        return BaguetteFile.__BaguetteMetadata(self, self.__modified_metadata_context_manager)
    
    @property
    def __metadata_size(self) -> int:
        """
        Internal function that returns the amount of bytes to write the metadata into the BaguetteFile. Use to create the data pointers.
        """
        try:
            str_metadata = f"{BaguetteFile.UNIX_EXEC_SCRIPT}\n{BaguetteFile.BAGUETTE_HEADER}\n{BaguetteFile.__jdumps(self.__metadata.export_dict(), indent="\t")}\n"
        except:
            return False
        return len(str_metadata.encode()) + BaguetteFile.POINTER_BYTE_SIZE * (len(self.__get_pointers()))
    
    def __write_metadata(self, file : BinaryIO) -> __Sector[BinaryIO]:
        """
        Internal function to write the metadata to the given file.
        Returns the data sector over that file descriptor.
        """
        file.seek(0)
        file.write(f"{BaguetteFile.UNIX_EXEC_SCRIPT}\n{BaguetteFile.BAGUETTE_HEADER}\n{BaguetteFile.__jdumps(self.__metadata.export_dict(), indent="\t")}\n".encode())
        file.write(b"".join(pos.to_bytes(BaguetteFile.POINTER_BYTE_SIZE, "little", signed = True) for pos in (self.__get_pointers())))
        if (a := file.tell()) != (b := self.__metadata_size):
            raise BaguetteFormatError(f"Metadata size mismatch after writing: got {a}, expected {b}", self.__path, self.__metadata)
        self.__data_fd = BaguetteFile.__Sector(file, a)
        self.__disk_metadata_size = a
        self.__modified_metadata = False
        file.flush()
        return self.__data_fd
    
    @property
    def path(self) -> __Path:
        """
        The path to the BaguetteFile.
        """
        return self.__path
    
    @property
    def readonly(self) -> bool:
        """
        Indicates if the BaguetteFile has been opened in readonly mode.
        """
        return self.__readonly
            
    def __rewrite_data(self, tmp_partition : __TMPStorage):
        """
        Internal function that erases all the data of the BaguetteFile, rewrites it from the content of the given temporary storage and changes the pointers in the metadata.
        """
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        self.__fd, self.__data_fd = self.__increase_disk_reference_count()

        try:
            self.__fd.truncate(0)
            pos = 0
            pointers : "dict[str, int]" = {}
            for name in tmp_partition.index:
                size = tmp_partition.size(name)
                self.__set_pointers(**{f"{name}_offset" : pos, f"{name}_size" : size})
                pointers[name] = pos
                pos += size
            
            self.__write_metadata(self.__fd)

            for name in sorted(pointers, key = lambda name : pointers[name]):
                self.__data_fd.seek(pointers[name])
                tmp_partition.load(self.__data_fd, name) 
            
            self.__fd.truncate()
            self.__fd.flush()

        finally:
            self.__decrease_disk_reference_count()

    def __rewrite_metadata(self):
        """
        Internal function that rewrites just the metadata, pushing the data around in the way.
        """
        if self.__readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        self.__fd, self.__data_fd = self.__increase_disk_reference_count()

        try:
            old_pos = self.__data_fd.window.start
            new_pos = self.__metadata_size
            delta_pos = new_pos - old_pos
            if new_pos > old_pos:
                end_pos = self.__fd.seek(0, BaguetteFile.__SEEK_END)
                old_positions = reversed(range(old_pos, end_pos, BaguetteFile.COPY_PACKET_SIZE))
            elif new_pos < old_pos:
                end_pos = self.__fd.seek(0, BaguetteFile.__SEEK_END)
                old_positions = range(old_pos, end_pos, BaguetteFile.COPY_PACKET_SIZE)
            else:
                old_positions = ()
            for old_pos in old_positions:
                self.__fd.seek(old_pos)
                packet = self.__fd.read(BaguetteFile.COPY_PACKET_SIZE)
                if packet:
                    self.__fd.seek(old_pos + delta_pos)
                    self.__fd.write(packet)
            self.__data_fd = self.__write_metadata(self.__fd)

        finally:
            self.__decrease_disk_reference_count()

    def __save_data(self, fields : Iterable[Literal["report", "graph_cache", "baguette", "patterns", "meta_cache", "matches", "dict"]], storage : __TMPStorage):
        """
        Internal function that saves the given fields if they exist of data into a given temporary storage.
        """
        if self.__readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        self.__fd, self.__data_fd = self.__increase_disk_reference_count()

        try:
            for name in fields:
                pos, size = self.__get_pointers(name)
                if pos >= 0:
                    self.__data_fd.seek(pos)
                    storage.save(self.__data_fd, name, size)
        
        finally:
            self.__decrease_disk_reference_count()

    def __enter__(self) -> Self:
        """
        Implements with self. Keeps the BaguetteFile open on disk while in the context.
        """
        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        return self
    
    def __exit__(self, exc : BaseException | None, exc_type : type[BaseException] | None, traceback : TracebackType | None):
        """
        Implements with self.
        """
        self.__decrease_disk_reference_count()

    def __initialize_pickler(self) -> __CachingPickler:
        """
        Internal function that initializes and returns the pickler for cross referencing objects between different sections.
        """
        if self.__pickler is None:
            self.__pickler = BaguetteFile.__CachingPickler()

        return self.__pickler

    def __initialize_unpickler(self) -> __CachingUnpickler:
        """
        Internal function that initializes and returns the unpickler for cross referencing objects between different sections.
        """
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if self.__unpickler is None:
            self.__fd, self.__data_fd = self.__increase_disk_reference_count()

            try:
                self.__unpickler = unpickler = BaguetteFile.__CachingUnpickler()
                if (pos := self.__graph_cache_offset) >= 0:
                    with BaguetteFile.__BZ2File(BaguetteFile.__SectorReader(self.__data_fd, pos, pos + self.__graph_cache_size), "rb") as f:
                        unpickler.set_input(f)
                        unpickler.load_cache()
                if (pos := self.__meta_cache_offset) >= 0:
                    with BaguetteFile.__BZ2File(BaguetteFile.__SectorReader(self.__data_fd, pos, pos + self.__meta_cache_size), "rb") as f:
                        unpickler.set_input(f)
                        unpickler.load_cache()
            
            finally:
                self.__decrease_disk_reference_count()
        
        return self.__unpickler

    @property
    def data(self) -> __Data:
        """
        A dict-like object to store many kind of information.
        All written data must be hashable and json-serializable.
        """
        if self.__dict is None:
            if (pos := self.__dict_offset) < 0:
                self.__dict = BaguetteFile.__Data(self.__update_data_dict)
            else:

                self.__fd, self.__data_fd = self.__increase_disk_reference_count()
                try:
                    with BaguetteFile.__BZ2File(BaguetteFile.__SectorReader(self.__data_fd, pos, pos + self.__dict_size), "rb") as f:
                        state = BaguetteFile.__jloads(f.read().decode())
                        if not isinstance(state, dict):
                            raise BaguetteFormatError(f"data dict is not a dict but a '{type(state).__name__}'", self.path, self.__metadata)
                        self.__dict = BaguetteFile.__Data(self.__update_data_dict, **state)
                except:
                    raise BaguetteFormatError("Corrupted data dict", self.path, self.__metadata)
                
                finally:
                    self.__decrease_disk_reference_count()
            
        return self.__dict
    
    def __update_data_dict(self):
        """
        Internal function used to update the data dictionary on disk.
        """
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        tmp = BaguetteFile.__TMPStorage()
        if self.__dict:
            def fix_data(obj):
                if isinstance(obj, BaguetteFile.__Data):
                    return obj.dump()
                return obj
            with BaguetteFile.__BZ2File(tmp.file_writer("dict"), "wb") as f:
                f.write(BaguetteFile.__jdumps(self.__dict, default=fix_data).encode())
        else:
            self.__set_pointers(dict_offset=-1, dict_size=0)

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            self.__save_data(["report", "baguette", "graph_cache", "patterns", "meta_cache", "matches"], tmp)
            self.__rewrite_data(tmp)

        finally:
            self.__decrease_disk_reference_count()

    def has_report(self) -> bool:
        """
        Returns True if the BaguetteFile has an affected report.
        """
        self.__reload_metatada_on_change()
        return self.__report_offset >= 0
    
    @property
    def report(self) -> __CodecStream:
        """
        The input execution report used to build the BAGUETTE Graph.
        Careful: setting or deleting this erases the BAGUETTE Graph and all match data.
        """
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if self.__report is not None:
            return BaguetteFile.__CodecStream(self.__report)
        if (pos := self.__report_offset) < 0:
            raise BaguetteFormatError("BaguetteFile report has not been set yet", self.path, self.__metadata)
        try:
            self.__fd, self.__data_fd = self.__increase_disk_reference_count()
            self.__data_fd.seek(pos + self.__report_size - BaguetteFile.POINTER_BYTE_SIZE)
            size = int.from_bytes(self.__data_fd.read(BaguetteFile.POINTER_BYTE_SIZE), "little")
            f = BaguetteFile.__SectorReader(BaguetteFile.__BZ2File(BaguetteFile.__SectorReader(self.__data_fd, pos, pos + self.__report_size - BaguetteFile.POINTER_BYTE_SIZE), "rb"), 0, size)
            self.__report = f
            return BaguetteFile.__CodecStream(f)
        except:
            raise BaguetteFormatError("Corrupted report", self.path, self.__metadata)
        
    @report.setter
    def report(self, report : __Path | __BytesReadable | __Buffer):
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if not isinstance(report, BaguetteFile.__Path | BaguetteFile.__BytesReadable | BaguetteFile.__Buffer):
            raise TypeError(f"Expected Path to a readable file, a file-like object or an object that supports the buffer protocol, got '{type(report).__name__}'")
        tmp = BaguetteFile.__TMPStorage()
        if isinstance(report, BaguetteFile.__Path):
            report = report.open("rb")
        tmp_writer = tmp.file_writer("report")
        with BaguetteFile.__BZ2File(tmp_writer, "wb") as f_dest:

            if isinstance(report, BaguetteFile.__BytesReadable):
                packet = True
                size = 0
                while packet:
                    packet = report.read(BaguetteFile.COPY_PACKET_SIZE)
                    size += len(packet)
                    f_dest.write(packet)

            else:
                packet = True
                size = 0
                report = report.__buffer__(BaguetteFile.__BufferFlags.SIMPLE | BaguetteFile.__BufferFlags.C_CONTIGUOUS)
                while packet:
                    packet = report[size : max(size + BaguetteFile.COPY_PACKET_SIZE, len(report))]
                    size += len(packet)
                    f_dest.write(packet)

        tmp_writer.write(size.to_bytes(BaguetteFile.POINTER_BYTE_SIZE, "little"))
        del tmp_writer

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            if self.__report is not None:
                self.__report.stream.close()
                self.__report = None
                self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
            self.__save_data(["dict", "patterns", "meta_cache"], tmp)
            self.__baguette = None
            self.__filtered_baguette = None
            if self.__matches:
                self.__matches.disable()
                self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
            self.__set_pointers(baguette_offset = -1, baguette_size = 0, matches_offset = -1, matches_size = 0)
            self.__pickler = None
            self.__unpickler = None
            self.__matches = None
            self.__rewrite_data(tmp)
            self.__report = BaguetteFile.__SectorReader(BaguetteFile.__BZ2File(BaguetteFile.__SectorReader(self.__data_fd, self.__report_offset, self.__report_offset + self.__report_size), "rb"), 0, size)
        except:
            if self.__report is None:
                self.__decrease_disk_reference_count()

    @report.deleter
    def report(self):
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        tmp = BaguetteFile.__TMPStorage()

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            self.__save_data(["dict", "patterns", "meta_cache"], tmp)
            self.__baguette = None
            self.__filtered_baguette = None
            if self.__matches:
                self.__matches.disable()
                self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
            if self.__report is not None:
                self.__report.stream.close()
                self.__report = None
                self.__decrease_disk_reference_count()
            self.__set_pointers(report_offset = -1, report_size = 0, baguette_offset = -1, baguette_size = 0, matches_offset = -1, matches_size = 0)
            self.__pickler = None
            self.__unpickler = None
            self.__matches = None
            self.__rewrite_data(tmp)

        finally:
            self.__decrease_disk_reference_count()

    def has_baguette(self) -> bool:
        """
        Returns True if the BaguetteFile has a baked BAGUETTE Graph.
        """
        return self.__baguette_offset >= 0

    @property
    def baguette(self) -> __FrozenGraph:
        """
        The compiled BAGUETTE Graph itself.
        Careful: setting or deleting this erases the match data.
        """
        if self.__baguette is not None:
            return self.__baguette
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if (pos := self.__baguette_offset) < 0:
            raise BaguetteFormatError("BAGUETTE has not been baked yet", self.path, self.__metadata)
        
        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            unpickler = self.__initialize_unpickler()
            self.__data_fd.seek(pos)
            with BaguetteFile.__BZ2File(BaguetteFile.__SectorReader(self.__data_fd, pos, pos + self.__baguette_size), "rb") as f:
                unpickler.set_input(f)
                bag = unpickler.load()
                if not isinstance(bag, BaguetteFile.__FrozenGraph):
                    raise BaguetteFormatError(f"BAGUETTE Graph is not a FrozenGraph but a '{type(bag).__name__}'", self.path, self.__metadata)
                self.__baguette = bag
                return bag
        except:
            raise BaguetteFormatError("Corrupted BAGUETTE Graph", self.path, self.__metadata)
        
        finally:
            self.__decrease_disk_reference_count()
            
    @baguette.setter
    def baguette(self, baguette : __Graph):
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if isinstance(baguette, BaguetteFile.__Graph) and not isinstance(baguette, BaguetteFile.__FrozenGraph):
            baguette = BaguetteFile.__FrozenGraph(baguette)
        if not isinstance(baguette, BaguetteFile.__FrozenGraph):
            raise TypeError(f"Expected FrozenGraph, got '{type(baguette).__name__}'")
        tmp = BaguetteFile.__TMPStorage()
        pickler = self.__initialize_pickler()
        with BaguetteFile.__BZ2File(tmp.file_writer("baguette"), "wb") as f:
            pickler.set_output(f)
            pickler.dump(baguette)
        if pat := self.patterns:
            with BaguetteFile.__BZ2File(tmp.file_writer("patterns"), "wb") as f:
                pickler.set_output(f)
                for p in pat:
                    if p not in pickler:
                        pickler.cache(p, "meta_cache")
                    for e in p:
                        if e not in pickler:
                            pickler.cache(e, "meta_cache")
                pickler.dump(pat)
            if "meta_cache" in pickler.cache_sections:
                with BaguetteFile.__BZ2File(tmp.file_writer("meta_cache"), "wb") as f:
                    pickler.set_output(f)
                    pickler.dump_cache("meta_cache")

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            self.__save_data(["dict", "report"], tmp)
            if self.__matches:
                self.__matches.disable()
                self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
            self.__set_pointers(matches_offset = -1, matches_size = 0)
            self.__pickler = None
            self.__unpickler = None
            self.__baguette = baguette
            self.__matches = None
            self.__rewrite_data(tmp)

        finally:
            self.__decrease_disk_reference_count()

    @baguette.deleter
    def baguette(self):
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        tmp = BaguetteFile.__TMPStorage()
        pickler = self.__initialize_pickler()
        if pat := self.patterns:
            with BaguetteFile.__BZ2File(tmp.file_writer("patterns"), "wb") as f:
                pickler.set_output(f)
                for p in pat:
                    if p not in pickler:
                        pickler.cache(p, "meta_cache")
                    for e in p:
                        if e not in pickler:
                            pickler.cache(e, "meta_cache")
                pickler.dump(pat)
            if "meta_cache" in pickler.cache_sections:
                with BaguetteFile.__BZ2File(tmp.file_writer("meta_cache"), "wb") as f:
                    pickler.set_output(f)
                    pickler.dump_cache("meta_cache")

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            self.__save_data(["dict", "report"], tmp)
            if self.__matches:
                self.__matches.disable()
                self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
            self.__set_pointers(baguette_offset = -1, baguette_size = 0, matches_offset = -1, matches_size = 0)
            self.__pickler = None
            self.__unpickler = None
            self.__baguette = None
            self.__filtered_baguette = None
            self.__matches = None
            self.__rewrite_data(tmp)

        finally:
            self.__decrease_disk_reference_count()

    @property
    def patterns(self) -> frozenset[__FrozenMetaGraph]:
        """
        The patterns to search for in this BAGUETTE Graph.
        Careful: setting or deleting this erases the match data.
        """
        if self.__patterns is not None:
            return self.__patterns
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if (pos := self.__patterns_offset) < 0:
            return frozenset()
        
        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            unpickler = self.__initialize_unpickler()
            self.__data_fd.seek(pos)
            with BaguetteFile.__BZ2File(BaguetteFile.__SectorReader(self.__data_fd, pos, pos + self.__patterns_size), "rb") as f:
                unpickler.set_input(f)
                pat = unpickler.load()
                if not isinstance(pat, frozenset):
                    raise BaguetteFormatError(f"BAGUETTE patterns is not a frozenset but a '{type(pat).__name__}'", self.path, self.__metadata)
                for p in pat:
                    if not isinstance(p, BaguetteFile.__FrozenMetaGraph):
                        raise BaguetteFormatError(f"BAGUETTE patterns is not a frozenset of FrozenMetaGraph, got a '{type(p).__name__}'", self.path, self.__metadata)
                self.__patterns = frozenset(pat)
                return self.__patterns
        except:
            raise BaguetteFormatError("Corrupted BAGUETTE patterns", self.path, self.__metadata)
        
        finally:
            self.__decrease_disk_reference_count()
        
    @patterns.setter
    def patterns(self, patterns : Iterable[__MetaGraph]):
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if not isinstance(patterns, BaguetteFile.__Iterable):
            raise TypeError(f"Expected iterable, got '{type(patterns).__name__}'")
        patterns_cp : "list[BaguetteFile.__FrozenMetaGraph]" = []
        for i, e in enumerate(patterns):
            if not isinstance(e, BaguetteFile.__MetaGraph):
                raise TypeError(f"Expected iterable of MetaGraphs, got a '{type(e).__name__}'")
            if not isinstance(e, BaguetteFile.__FrozenMetaGraph):
                patterns_cp.append(BaguetteFile.__FrozenMetaGraph(e))
            else:
                patterns_cp.append(e)
        patterns_set = frozenset(patterns_cp)
        tmp = BaguetteFile.__TMPStorage()
        pickler = self.__initialize_pickler()
        with BaguetteFile.__BZ2File(tmp.file_writer("patterns"), "wb") as f:
            pickler.set_output(f)
            for p in patterns_set:
                if p not in pickler:
                    pickler.cache(p, "meta_cache")
                for e in p:
                    if e not in pickler:
                        pickler.cache(e, "meta_cache")
            pickler.dump(patterns_set)
        if "meta_cache" in pickler.cache_sections:
            with BaguetteFile.__BZ2File(tmp.file_writer("meta_cache"), "wb") as f:
                pickler.set_output(f)
                pickler.dump_cache("meta_cache")

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            self.__save_data(["dict", "report", "baguette", "graph_cache"], tmp)
            if self.__matches:
                self.__matches.disable()
                self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
            self.__set_pointers(matches_offset = -1, matches_size = 0)
            self.__pickler = None
            self.__unpickler = None
            self.__patterns = patterns_set
            self.__metadata.extraction_parameters.paint_color = None
            self.__matches = None
            self.__rewrite_data(tmp)
        
        finally:
            self.__decrease_disk_reference_count()

    @patterns.deleter
    def patterns(self):
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        tmp = BaguetteFile.__TMPStorage()

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            self.__save_data(["dict", "report", "baguette", "graph_cache"], tmp)
            if self.__matches:
                self.__matches.disable()
                self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
            self.__set_pointers(matches_offset = -1, matches_size = 0, patterns_offset = -1, patterns_size = 0)
            self.__pickler = None
            self.__unpickler = None
            self.__patterns = None
            self.__metadata.extraction_parameters.paint_color = None
            self.__matches = None
            self.__rewrite_data(tmp)

        finally:
            self.__decrease_disk_reference_count()

    def has_matches(self) -> bool:
        """
        Returns True if the BaguetteFile has an iterable of matches for its patterns.
        """
        return self.__matches_offset >= 0

    @property
    def matches(self) -> __MatchFileSequence | None:
        """
        The matches found for selected patterns in the BAGUETTE Graph. None if they have not been searched.
        You can set the matches to a given match iterable over all the matches of all the patterns in the BAGUETTE Graph.
        """
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if self.__matches is not None:
            return self.__matches
        if (pos := self.__matches_offset) < 0:
            return None
        try:
            self.__fd, self.__data_fd = self.__increase_disk_reference_count()
            self.__matches = BaguetteFile.__MatchFileSequence(BaguetteFile.__SectorReader(self.__data_fd, pos, pos + self.__matches_size), self.__initialize_unpickler())
            return self.__matches
        except:
            if self.__matches is None:
                self.__decrease_disk_reference_count()
            raise BaguetteFormatError("Corrupted BAGUETTE matches", self.path, self.__metadata)
        
    @matches.setter
    def matches(self, matches_iterable : Iterable[__FrozenMetaGraph.Match]):
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if not isinstance(matches_iterable, BaguetteFile.__Iterable):
            raise TypeError(f"Expected iterable, got '{type(matches_iterable).__name__}'")
        if self.__patterns is None:
            self.__patterns = self.patterns
        if self.__baguette is None:
            if self.has_baguette():
                self.__baguette = self.baguette
            else:
                raise RuntimeError("'baguette' attribute must be set before saving the matches in the same BAGUETTE Graph")
        if self.__matches:
            self.__matches.disable()
            self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
        matches_iterable = iter(matches_iterable)
        ids = {id(pat) for pat in self.__patterns}
        pickler = self.__initialize_pickler()
        tmp = BaguetteFile.__TMPStorage()
        tmp_matches = BaguetteFile.__TMPStorage()

        n_matches, pos = 0, 0
        positions : "dict[BaguetteFile.__MetaGraph, list[int]]" = {}

        with BaguetteFile.__BZ2File(tmp_matches.file_writer("matches"), "wb") as f_tmp:
            pickler.set_output(f_tmp)
            for match in matches_iterable:
                if id(match.metagraph) not in ids:
                    raise ValueError(f"Unknown MetaGraph: {match.metagraph}")
                if match.metagraph not in pickler:
                    pickler.cache(match.metagraph, "meta_cache")
                for e in match.metagraph:
                    if not e in pickler:
                        pickler.cache(e, "meta_cache")
                for e in match.graph:
                    if not e in pickler:
                        pickler.cache(e, "graph_cache")
                pickler.dump(match)
                positions.setdefault(match.metagraph, []).append(pos)
                pos = f_tmp.tell()
                n_matches += 1
            
        with BaguetteFile.__BZ2File(tmp_matches.file_writer("metadata"), "wb") as f:
            pickler.set_output(f)
            pickler.dump((positions, pos))

        metadata_size = tmp_matches.size("metadata")
        tmp.file_writer("matches").write(metadata_size.to_bytes(8, "little"))
        tmp.save(tmp_matches.file_reader("metadata"), "matches")
        tmp.save(tmp_matches.file_reader("matches"), "matches")

        with BaguetteFile.__BZ2File(tmp.file_writer("patterns"), "wb") as f:
            pickler.set_output(f)
            for p in self.__patterns:
                if p not in pickler:
                    pickler.cache(p, "meta_cache")
                for e in p:
                    if e not in pickler:
                        pickler.cache(e, "meta_cache")
            pickler.dump(self.__patterns)
        if "meta_cache" in pickler.cache_sections:
            with BaguetteFile.__BZ2File(tmp.file_writer("meta_cache"), "wb") as f:
                pickler.set_output(f)
                pickler.dump_cache("meta_cache")
        with BaguetteFile.__BZ2File(tmp.file_writer("baguette"), "wb") as f:
            pickler.set_output(f)
            pickler.dump(self.__baguette)
        if "graph_cache" in pickler.cache_sections:
            with BaguetteFile.__BZ2File(tmp.file_writer("graph_cache"), "wb") as f:
                pickler.set_output(f)
                pickler.dump_cache("graph_cache")

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            self.__save_data(["dict", "report"], tmp)
            self.__rewrite_data(tmp)
            self.__pickler = None
            self.__unpickler = None
            self.__matches = BaguetteFile.__MatchFileSequence(BaguetteFile.__SectorReader(self.__data_fd, self.__matches_offset, self.__matches_offset + self.__matches_size), self.__initialize_unpickler())
        
        except:
            if self.__matches is None:
                self.__decrease_disk_reference_count()

    @matches.deleter
    def matches(self):
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        if self.__patterns is None:
            self.__patterns = self.patterns
        if self.__baguette is None:
            if self.has_baguette():
                self.__baguette = self.baguette
            else:
                raise RuntimeError("'baguette' attribute must be set before saving the matches in the same BAGUETTE Graph")
        if self.__matches:
            self.__matches.disable()
            self.__decrease_disk_reference_count()      # We are supposed to go from 2 to 1
        pickler = self.__initialize_pickler()
        tmp = BaguetteFile.__TMPStorage()

        with BaguetteFile.__BZ2File(tmp.file_writer("patterns"), "wb") as f:
            pickler.set_output(f)
            for p in self.__patterns:
                if p not in pickler:
                    pickler.cache(p, "meta_cache")
                for e in p:
                    if e not in pickler:
                        pickler.cache(e, "meta_cache")
            pickler.dump(self.__patterns)
        if "meta_cache" in pickler.cache_sections:
            with BaguetteFile.__BZ2File(tmp.file_writer("meta_cache"), "wb") as f:
                pickler.set_output(f)
                pickler.dump_cache("meta_cache")
        with BaguetteFile.__BZ2File(tmp.file_writer("baguette"), "wb") as f:
            pickler.set_output(f)
            pickler.dump(self.__baguette)
        if "graph_cache" in pickler.cache_sections:
            with BaguetteFile.__BZ2File(tmp.file_writer("graph_cache"), "wb") as f:
                pickler.set_output(f)
                pickler.dump_cache("graph_cache")

        self.__fd, self.__data_fd = self.__increase_disk_reference_count()
        try:
            self.__save_data(["dict", "report"], tmp)
            self.__set_pointers(matches_offset = -1, matches_size = 0)
            self.__rewrite_data(tmp)
            self.__pickler = None
            self.__unpickler = None
            self.__matches = None

        finally:
            self.__decrease_disk_reference_count()

    def clean(self):
        """
        Removes all the data of the BaguetteFile. Leaves an empty BaguetteFile.
        """
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        del self.report
        del self.patterns

    @property
    def baking_exception(self) -> TracebackException | None:
        """
        The exception that occured during baking or None if baking went fine.
        """
        return self.metadata.compilation_parameters.exception
    
    @property
    def toasting_exception(self) -> TracebackException | None:
        """
        The exception that occured during toasting or None if toasting went fine.
        """
        return self.metadata.extraction_parameters.exception
    
    def add_named_patterns(self, *names : str):
        """
        Adds patterns which names are searched through the metalib.
        """
        if self.readonly:
            raise ValueError("BaguetteFile opened in read-only mode")
        if self.__closed:
            raise ValueError("BaguetteFile is closed")
        for name in names:
            if not isinstance(name, str):
                raise TypeError(f"Expected str, got '{type(name).__name__}'")
        from ..croutons.metalib import entries, load
        existing = set(entries())
        for name in names:
            if name not in existing:
                raise ValueError(f"MetaGraph not found in metalib: '{name}'")
        self.patterns = self.patterns | {load(name) for name in names}

    @property
    def visual_filters(self) -> list[Filter]:
        """
        The Filters to apply when generating the visual representation of the BAGUETTE Graph.
        When setting the filters, the elements of the given iterable can be either a Filter object or a Filter name.
        """
        from ..bakery.source.filters import Filter
        existing_filters = Filter.enumerate()
        l : "list[Filter]" = []
        for name in self.__metadata.compilation_parameters.filter_names:
            if name not in existing_filters:
                raise ValueError(f"Unkonwn filter: '{name}'")
            l.append(existing_filters[name])
        return l
    
    @visual_filters.setter
    def visual_filters(self, filters : Iterable[Filter | str]):
        if not isinstance(filters, BaguetteFile.__Iterable):
            raise TypeError(f"Expected iterable, got '{type(filters).__name__}'")
        from ..bakery.source.filters import Filter
        existing_filters = Filter.enumerate()
        filters = list(filters)
        filter_names : "list[str]" = []
        for e in filters:
            if not isinstance(e, str | Filter):
                raise TypeError(f"Expected iterable of str or Filter, got a '{type(e).__name__}'")
            if isinstance(e, str):
                if e not in existing_filters:
                    raise ValueError(f"Unknown Filter name: '{e}'")
                filter_names.append(e)
            else:
                if e.name not in existing_filters:
                    raise ValueError(f"Unknown Filter: '{e}'")
                filter_names.append(e.name)
        self.__metadata.compilation_parameters.filter_names = filter_names

    @property
    def filtered_baguette(self) -> __Graph:
        """
        Returns the Graph after applying the visual filters set in the BaguetteFile metadata.
        """
        if self.__filtered_baguette is None:
            g = self.baguette
            for f in self.visual_filters:
                g = f.apply(g)
            self.__filtered_baguette = g
        return self.__filtered_baguette
    
    @property
    def baked(self) -> bool:
        """
        Returns True if a complete baking attempt was made (i.e. if the BAGUETTE was successfully baked or if the compilation failed for another reason than a timeout or an interruption).
        If False, trying to bake it (again) makes sense.
        """
        from ..bakery.compiler import BakingTimeout
        return self.has_baguette() or (self.metadata.compilation_parameters.exception is not None and not issubclass(self.metadata.compilation_parameters.exception.exc_type, (KeyboardInterrupt, BakingTimeout)))

    @property
    def toasted(self) -> bool:
        """
        Returns True if a complete toasting attempt was made (i.e. if the BAGUETTE was successfully toasted or if the extraction failed for another reason than a timeout or an interruption).
        If False, trying to toast it (again) makes sense.
        """
        from ..bakery.compiler import BakingTimeout
        return self.has_matches() or (self.metadata.extraction_parameters.exception is not None and not issubclass(self.metadata.extraction_parameters.exception.exc_type, (KeyboardInterrupt, BakingTimeout)))





def is_baguette_file(file : Path | str) -> bool:
    """
    Checks if the given file is a BAGUETTE file.
    """
    return BaguetteFile.is_baguette_file(file)



del Path, Any, Iterable, Literal, overload, TracebackException, BinaryIO, TracebackType, Self, ExitCode, MetadataContextManager, Callable