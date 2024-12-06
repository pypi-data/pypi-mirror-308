"""
This module declares the metadata handling structures for the BAGUETTE file format.
"""

from traceback import TracebackException
from types import TracebackType
from typing import Any, Callable, Iterable, Literal, TYPE_CHECKING, Protocol, overload
if TYPE_CHECKING:
    from .baguette_file import BaguetteFile

__all__ = ["CompilationParameters", "ExtractionParameters", "BaguetteMetadata"]





class PropertyClass:

    """
    A base class that allows the enumeration of properties with their values.
    """

    def fields(self) -> Iterable[tuple[str, Any]]:
        """
        Yields all the pairs (field, value) for all fields of this object.
        """
        for name in self.field_names():
            yield name, getattr(self, name)

    def field_names(self) -> Iterable[str]:
        """
        Yields all the field names of this object.
        """
        for name in sorted(dir(self), key = lambda name : ("offset" not in name and "size" not in name, name)):
            try:
                if isinstance(getattr(type(self), name), property):
                    yield name
            except AttributeError:
                continue





class MetadataContextManager(Protocol):

    """
    A protocol for context manager objects used when modifying metadata.
    """

    def __enter__(self):
        """
        Enters the context of metadata modification.
        Should raise an exception if metadata cannot be modified.
        """
    
    @overload
    def __exit__(self, exc_type : None, exc : None, traceback : None):
        ...

    @overload
    def __exit__[E : BaseException](self, exc_type : type[E], exc : E, traceback : TracebackType):
        ...
    
    def __exit__[E : BaseException](self, exc_type : type[E] | None = None, exc : E | None = None, traceback : TracebackType | None = None):
        """
        Exits the context of metadata modification.
        Actions can now be taken regarding this.
        """





class CompilationParameters(PropertyClass):

    """
    A data structure to hold all the compilation metadata of a BAGUETTE file.
    Do not modify yourself properties starting with a single underscore!
    """

    from ast import literal_eval
    from pickle import dumps, loads
    from traceback import TracebackException as __TracebackException
    from typing import Iterable as __Iterable
    from ..bakery.source.colors import Color as __Color
    __literal_eval = staticmethod(literal_eval)
    __dumps = staticmethod(dumps)
    __loads = staticmethod(loads)
    del literal_eval, dumps, loads

    __slot__ = {
        "__file" : "The BAGUETTE file that has these compilation parameters",
        "__update_context" : "A MetadataContextManager to call to signal the BAGUETTE file that a parameter has been modified and must be written to disk again",
        "__perf" : "If True a performance report is printed after compiling",
        "__filter_names" : "The names of the filters to apply when exporting the BAGUETTE Graph to GEXF format",
        "__skip_data_comparison" : "If True, comparison of Data vertices will be skipped (and all be considered unrelated)",
        "__skip_diff_comparison" : "If True, comparison of Diff vertices will be skipped (and all be considered unrelated)",
        "__exception" : "An eventual exception that occured during the compilation of this BAGUETTE",
        "__verbosity" : "The verbosity level applied during compilation",
        "__timeout" : "The timeout to apply during the compilation",
        "__suppressed" : "If True and an exception occurs during the compilation, the BAGUETTE file will be removed",
        "__background_color" : "The color of the background for visual rendering",
        "__report_type" : "The type of the input report used to compile this BAGUETTE Graph"
    }

    def __init__(self,
                 file : "BaguetteFile",
                 update_context : MetadataContextManager,
                 perf : bool = False,
                 filter_names : __Iterable[str] = (),
                 skip_data_comparison : bool = False,
                 skip_diff_comparison : bool = False,
                 exception : TracebackException | None = None,
                 verbosity : Literal[0, 1, 2, 3] = 0,
                 timeout : float = float("inf"),
                 suppressed : bool = False,
                 background_color : __Color = __Color.black,
                 report_type : str | None = None
                 ) -> None:
        self.__file = file
        self.__update_context = update_context
        self.perf = perf
        self.filter_names = filter_names
        self.skip_data_comparison = skip_data_comparison
        self.skip_diff_comparison = skip_diff_comparison
        self.exception = exception
        self.verbosity = verbosity
        self.timeout = timeout
        self.suppressed = suppressed
        self.background_color = background_color
        self.report_type = report_type

    def export_dict(self) -> dict[str, Any]:
        """
        Exports the metadata as a dictionary for saving.
        """
        data = {name : value for name, value in self.fields()}
        data["exception"] = self.exception if self.exception is None else repr(CompilationParameters.__dumps(self.exception))
        data["background_color"] = self.background_color if self.background_color is None else list(self.background_color)
        return data
    
    def import_dict(self, data : dict[str, Any]):
        """
        Imports the metadata from a saved dictionary.
        """
        data["exception"] = data["exception"] if data["exception"] is None else CompilationParameters.__loads(CompilationParameters.__literal_eval(data["exception"]))
        data["background_color"] = data["background_color"] if data["background_color"] is None else CompilationParameters.__Color(*data["background_color"])
        for name in self.field_names():
            setattr(self, name, data[name])

    @property
    def perf(self) -> bool:
        """
        If True, a performance report will be printed at the end of the compilation.
        """
        return self.__perf
    
    @perf.setter
    def perf(self, perf : bool):
        with self.__update_context:
            if not isinstance(perf, bool):
                raise TypeError(f"Expected bool, got '{type(perf).__name__}'")
            self.__perf = perf

    @property
    def filter_names(self) -> list[str]:
        """
        The list of filter names to use when generating the Gephi visual (.gexf file).
        """
        return self.__filter_names
    
    @filter_names.setter
    def filter_names(self, filter_names : __Iterable[str]):
        with self.__update_context:
            if not isinstance(filter_names, CompilationParameters.__Iterable):
                raise TypeError(f"Expected iterable, got '{type(filter_names).__name__}'")
            filter_names = list(filter_names)
            for f in filter_names:
                if not isinstance(f, str):
                    raise TypeError(f"Expected iterable of str, got a '{type(f).__name__}'")
            self.__filter_names = filter_names

    @filter_names.deleter
    def filter_names(self):
        self.filter_names = []

    @property
    def skip_data_comparison(self) -> bool:
        """
        If True, comparison of Data vertices will be skipped. No similarity link will exist between those.
        """
        return self.__skip_data_comparison
    
    @skip_data_comparison.setter
    def skip_data_comparison(self, skip_data_comparison : bool):
        with self.__update_context:
            if not isinstance(skip_data_comparison, bool):
                raise TypeError(f"Expected bool, got '{type(skip_data_comparison).__name__}'")
            self.__skip_data_comparison = skip_data_comparison

    @property
    def skip_diff_comparison(self) -> bool:
        """
        If True, comparison of Diff vertices will be skipped. No similarity link will exist between those.
        """
        return self.__skip_diff_comparison
    
    @skip_diff_comparison.setter
    def skip_diff_comparison(self, skip_diff_comparison : bool):
        with self.__update_context:
            if not isinstance(skip_diff_comparison, bool):
                raise TypeError(f"Expected bool, got '{type(skip_diff_comparison).__name__}'")
            self.__skip_diff_comparison = skip_diff_comparison

    @property
    def exception(self) -> TracebackException | None:
        """
        The optional exception that could have occured during the compilation of this BAGUETTE Graph.
        """
        return self.__exception
    
    @exception.setter
    def exception(self, exception : TracebackException | None):
        with self.__update_context:
            if exception is not None and not isinstance(exception, CompilationParameters.__TracebackException):
                raise TypeError(f"Excepected TracebackException or None, got '{type(exception)}'")
            self.__exception = exception

    @exception.deleter
    def exception(self):
        self.exception = None

    @property
    def verbosity(self) -> Literal[0, 1, 2, 3]:
        """
        The verbosity level to use when compiling the BAGUETTE Graph.
        """
        return self.__verbosity
    
    @verbosity.setter
    def verbosity(self, verbosity : Literal[0, 1, 2, 3]):
        with self.__update_context:
            if not isinstance(verbosity, int):
                raise TypeError(f"Expected int, got '{type(verbosity).__name__}'")
            if verbosity not in (0, 1, 2 ,3):
                raise ValueError(f"Expected value in (0, 1, 2, 3), got {verbosity}")
            self.__verbosity : "Literal[0, 1, 2, 3]" = verbosity

    @property
    def timeout(self) -> float:
        """
        The timeout after which the compilation of this BAGUETTE Graph should be cancelled.
        """
        return self.__timeout
    
    @timeout.setter
    def timeout(self, timeout : float):
        with self.__update_context:
            if isinstance(timeout, int):
                timeout = float(timeout)
            if not isinstance(timeout, float):
                raise TypeError(f"Expected float, got '{type(timeout).__name__}'")
            if timeout < 0:
                raise ValueError(f"Expected positive float, got {timeout}")
            self.__timeout = timeout

    @timeout.deleter
    def timeout(self):
        self.timeout = float("inf")
    
    @property
    def suppressed(self) -> bool:
        """
        If True, the BAGUETTE file is deleted if an error occurs during compilation.
        """
        return self.__suppressed
    
    @suppressed.setter
    def  suppressed(self, suppressed : bool):
        with self.__update_context:
            if not isinstance(suppressed, bool):
                raise TypeError(f"Expected bool, got '{type(suppressed).__name__}'")
            self.__suppressed = suppressed

    @property
    def background_color(self) -> __Color:
        """
        The Color of the background when generating Gephi visual (.gexf file).
        This is used to optimize the Colors of certain vertices/edges to be more visible.
        """
        return self.__background_color
    
    @background_color.setter
    def background_color(self, background_color : __Color):
        with self.__update_context:
            if not isinstance(background_color, CompilationParameters.__Color):
                raise TypeError(f"Expected Color, got '{type(background_color).__name__}'")
            self.__background_color = background_color
    
    @property
    def report_type(self) -> str | None:
        """
        The type of input execution report used for compiling this BAGUETTE Graph.
        None if it is still unknown.
        """
        return self.__report_type
    
    @report_type.setter
    def report_type(self, report_type : str | None):
        with self.__update_context:
            if report_type is not None and not isinstance(report_type, str):
                raise TypeError(f"Expected str or None, got '{type(report_type).__name__}'")
            self.__report_type = report_type
    
    @report_type.deleter
    def report_type(self):
        self.report_type = None





class ExtractionParameters(PropertyClass):

    """
    A data structure to hold the extraction metadata of a BAGUETTE file.
    Do not modify yourself properties starting with a single underscore!
    """

    from ast import literal_eval
    from pickle import dumps, loads
    from traceback import TracebackException as __TracebackException
    from typing import Iterable as __Iterable
    from ..bakery.source.colors import Color as __Color
    __literal_eval = staticmethod(literal_eval)
    __dumps = staticmethod(dumps)
    __loads = staticmethod(loads)
    del literal_eval, dumps, loads

    __slots__ = {
        "__file" : "The BAGUETTE file that has these extraction parameters",
        "__update_context" : "A MetadataContextManager to call to signal the BAGUETTE file that a parameter has been modified and must be written to disk again",
        "__perf" : "If True a performance report is printed after extraction",
        "__exception" : "An eventual exception that occured during the extraction of patterns for this BAGUETTE file",
        "__verbosity" : "The verbosity level applied during extraction",
        "__timeout" : "The timeout to apply during the extraction",
        "__suppressed" : "If True and an exception occurs during the extraction, the BAGUETTE file will be removed",
        "__paint_color" : "A Color used to replace the painting colors of the MetaGraph patterns"
    }

    def __init__(self,
                 file : "BaguetteFile",
                 update_context : MetadataContextManager,
                 perf : bool = False,
                 exception : TracebackException | None = None,
                 verbosity : Literal[0, 1, 2, 3] = 0,
                 timeout : float = float("inf"),
                 suppressed : bool = False,
                 paint_color : __Color | Literal[False] | None = None
                 ) -> None:
        self.__file = file
        self.__update_context = update_context
        self.perf = perf
        self.exception = exception
        self.verbosity = verbosity
        self.timeout = timeout
        self.suppressed = suppressed
        self.paint_color = paint_color

    def export_dict(self) -> dict[str, Any]:
        """
        Exports the metadata as a dictionary for saving.
        """
        data = {name : value for name, value in self.fields()}
        data["exception"] = self.exception if self.exception is None else repr(ExtractionParameters.__dumps(self.exception))
        data["paint_color"] = self.paint_color if self.paint_color is None or self.paint_color is False else list(self.paint_color)
        return data
    
    def import_dict(self, data : dict[str, Any]):
        """
        Imports the metadata from a saved dictionary.
        """
        data["exception"] = data["exception"] if data["exception"] is None else ExtractionParameters.__loads(ExtractionParameters.__literal_eval(data["exception"]))
        data["paint_color"] = data["paint_color"] if data["paint_color"] is None or data["paint_color"] is False else ExtractionParameters.__Color(*data["paint_color"])
        for name in self.field_names():
            setattr(self, name, data[name])

    @property
    def perf(self) -> bool:
        """
        If True, a performance report will be printed at the end of the compilation.
        """
        return self.__perf
    
    @perf.setter
    def perf(self, perf : bool):
        with self.__update_context:
            if not isinstance(perf, bool):
                raise TypeError(f"Expected bool, got '{type(perf).__name__}'")
            self.__perf = perf

    @property
    def exception(self) -> TracebackException | None:
        """
        The optional exception that could have occured during the extraction of patterns in this BAGUETTE file.
        """
        return self.__exception
    
    @exception.setter
    def exception(self, exception : TracebackException | None):
        with self.__update_context:
            if exception is not None and not isinstance(exception, ExtractionParameters.__TracebackException):
                raise TypeError(f"Excepected TracebackException or None, got '{type(exception)}'")
            self.__exception = exception

    @exception.deleter
    def exception(self):
        self.exception = None

    @property
    def verbosity(self) -> Literal[0, 1, 2, 3]:
        """
        The verbosity level to use when extracting patterns from the BAGUETTE file.
        """
        return self.__verbosity
    
    @verbosity.setter
    def verbosity(self, verbosity : Literal[0, 1, 2, 3]):
        with self.__update_context:
            if not isinstance(verbosity, int):
                raise TypeError(f"Expected int, got '{type(verbosity).__name__}'")
            if verbosity not in (0, 1, 2 ,3):
                raise ValueError(f"Expected value in (0, 1, 2, 3), got {verbosity}")
            self.__verbosity : "Literal[0, 1, 2, 3]" = verbosity

    @property
    def timeout(self) -> float:
        """
        The timeout after which the extraction of patterns from this BAGUETTE file should be cancelled.
        """
        return self.__timeout
    
    @timeout.setter
    def timeout(self, timeout : float):
        with self.__update_context:
            if isinstance(timeout, int):
                timeout = float(timeout)
            if not isinstance(timeout, float):
                raise TypeError(f"Expected float, got '{type(timeout).__name__}'")
            if timeout < 0:
                raise ValueError(f"Expected positive float, got {timeout}")
            self.__timeout = timeout

    @timeout.deleter
    def timeout(self):
        self.timeout = float("inf")

    @property
    def suppressed(self) -> bool:
        """
        If True, the BAGUETTE file is deleted if an error occurs when searching for patterns.
        """
        return self.__suppressed
    
    @suppressed.setter
    def  suppressed(self, suppressed : bool):
        with self.__update_context:
            if not isinstance(suppressed, bool):
                raise TypeError(f"Expected bool, got '{type(suppressed).__name__}'")
            self.__suppressed = suppressed

    @property
    def paint_color(self) -> __Color | Literal[False] | None:
        """
        A Color used to replace the colors of the MetaGraph patterns.
        False indicates to skip painting.
        None means to keep the original pattern colors.
        """
        return self.__paint_color
    
    @paint_color.setter
    def paint_color(self, paint_color : __Color | Literal[False] | None):
        """
        Sets the replacement Color mode.
        """
        with self.__update_context:
            if paint_color is not None and paint_color is not False and not isinstance(paint_color, ExtractionParameters.__Color):
                raise TypeError(f"Expected None, False or Color, got '{type(paint_color).__name__}'")
            self.__paint_color : "ExtractionParameters.__Color | Literal[False] | None" = paint_color

    @paint_color.deleter
    def paint_color(self):
        self.paint_color = None
        




class BaguetteMetadata:

    """
    A data structure to hold the metadata of a BAGUETTE file.
    Do not modify yourself properties starting with a single underscore!
    """
    
    __slots__ = {
        "__file" : "The BAGUETTE file that has this metadata",
        "__update_context" : "A MetadataContextManager to call to signal the BAGUETTE file that a parameter has been modified and must be written to disk again",
        "__compilation_parameters" : "a 'CompilationParameters' object",
        "__extraction_parameters" : "a 'ExtractionParameters' object"
    }

    def __init__(self,
                 file : "BaguetteFile",
                 update_context : MetadataContextManager,
                 compilation_parameters : CompilationParameters | None = None,
                 extraction_parameters : ExtractionParameters | None = None
                 ) -> None:
        self.__file = file
        self.__update_context = update_context
        self.__compilation_parameters = compilation_parameters if compilation_parameters else CompilationParameters(file, update_context)
        self.__extraction_parameters = extraction_parameters if extraction_parameters else ExtractionParameters(file, update_context)

    @property
    def compilation_parameters(self) -> CompilationParameters:
        """
        The compilation parameters for this BAGUETTE file.
        """
        return self.__compilation_parameters
    
    @property
    def extraction_parameters(self) -> ExtractionParameters:
        """
        The extraction parameters for this BAGUETTE file.
        """
        return self.__extraction_parameters
    
    def export_dict(self) -> dict[str, dict]:
        """
        Exports the metadata as a dictionary for saving.
        """
        return {
            "compilation_parameters" : self.compilation_parameters.export_dict(),
            "extraction_parameters" : self.extraction_parameters.export_dict()
        }
    
    def import_dict(self, data : dict[str, dict]):
        """
        Imports the metadata from a saved dictionary.
        """
        if "compilation_parameters" in data:
            self.compilation_parameters.import_dict(data["compilation_parameters"])
        if "extraction_parameters" in data:
            self.extraction_parameters.import_dict(data["extraction_parameters"])





del TracebackException, Any, Callable, Iterable, Literal, TYPE_CHECKING, PropertyClass, TracebackType, Protocol, overload