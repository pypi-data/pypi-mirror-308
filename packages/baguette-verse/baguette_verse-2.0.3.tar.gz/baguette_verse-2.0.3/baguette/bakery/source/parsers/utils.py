"""
This module adds some useful tools for parsers, especially for translating API calls.
"""

from collections.abc import Iterable
from pathlib import Path
from typing import Any, TYPE_CHECKING, Callable, Literal
if TYPE_CHECKING:
    from .abc import CallInfo

__all__ = ["Translator", "MissingBehavioralInfoError", "MissingSamplePathError"]





class Translator:

    """
    A Translator is used to translate API call registered from a given source into a BAGUETTE compatible version.
    The most important part of this process is translating API call parameter names.
    """

    import json as __json
    from pathlib import Path as __Path

    @staticmethod
    def protected_hex(i):
        try:
            return hex(i)
        except:
            return i
        
    @staticmethod
    def protected_str(i):
        try:
            return str(i)
        except:
            return i
        
    @staticmethod
    def protected_int(s):
        try:
            return int(s)
        except:
            return s
        
    @staticmethod
    def protected_int16(s):
        try:
            return int(s, base=16)
        except:
            return s

    ARGUMENT_CONVERTERS = {
        "int_to_hex" : protected_hex,
        "int_to_str" : protected_str,
        "str_to_int" : protected_int,
        "hex_to_int" : protected_int16
    }

    del protected_int16, protected_int, protected_str, protected_hex

    FUNC_NAMES = Literal["int_to_hex", "int_to_str", "str_to_int", "hex_to_int"]



    class StrDict[K : str, V : str](dict[K, V]):

        """
        A subclass of dict that only allows str keys and values.
        """

        from pathlib import Path as __Path

        def __init__(self, iterable = (), **kwargs):
            super().__init__(iterable, **kwargs)
            for k, v in self.items():
                if not isinstance(k, str):
                    raise TypeError(f"Expected str keys, got a '{type(k).__name__}'")
                if not isinstance(v, str):
                    raise TypeError(f"Expected str values, got a '{type(v).__name__}'")
                
        def __setitem__(self, k: K, v: V) -> None:
            if not isinstance(k, str):
                raise TypeError(f"Expected str keys, got a '{type(k).__name__}'")
            if not isinstance(v, str):
                raise TypeError(f"Expected str values, got a '{type(v).__name__}'")
            return super().__setitem__(k, v)
        
        def get(self, k : K, default : V = "") -> V: # type: ignore
            if not isinstance(k, str):
                raise TypeError(f"Expected str keys, got a '{type(k).__name__}'")
            if not isinstance(default, str):
                raise TypeError(f"Expected str keys, got a '{type(default).__name__}'")
            return super().get(k, default)
        
        def setdefault(self, k : K, default : V = "") -> V: # type: ignore
            if not isinstance(k, str):
                raise TypeError(f"Expected str keys, got a '{type(k).__name__}'")
            if not isinstance(default, str):
                raise TypeError(f"Expected str keys, got a '{type(default).__name__}'")
            return super().setdefault(k, default)
        
        def copy(self):
            return Translator.StrDict(self)
        
        def update(self, mapping : dict[K, V], **kwargs : V):
            mapping = Translator.StrDict(mapping) | Translator.StrDict(kwargs)
            super().update(mapping)
        
        @classmethod
        def fromkeys(cls, keys : Iterable[K], value : V = ""): # type: ignore
            return cls((k, value) for k in keys)



    class CallTranslation:

        """
        A class to handle the translation of a single API call more easily.
        """

        def __init__(self, translator : "Translator", name : str, argument_name_table : "Translator.StrDict", argument_converters : "Translator.StrDict") -> None:
            self.__translator = translator
            self.__name = name
            self.__argument_name_table = argument_name_table
            self.__argument_converters = argument_converters

        def __str__(self) -> str:
            return f"<{self.name} translation: args[{', '.join(f'{k} -> {v}' for k, v in self.args.items())}]>"

        @property
        def name(self) -> str:
            """
            The name of this API call's translation.
            """
            return self.__name
        
        @property
        def translator(self) -> "Translator":
            """
            The Translator this translation is part of.
            """
            return self.__translator
        
        @property
        def argument_codex(self) -> "Translator.StrDict":
            """
            The translation table for this call's argument names.
            """
            return self.__argument_name_table
        
        @argument_codex.setter
        def argument_codex(self, codex : dict[str, str]):
            if isinstance(codex, dict):
                try:
                    codex = Translator.StrDict(codex)
                except:
                    raise TypeError("Expected dict with str keys and str values")
            if not isinstance(codex, Translator.StrDict):
                raise TypeError(f"Expected dict, got '{type(codex).__name__}'")
            self.__argument_name_table.clear()
            self.__argument_name_table.update(codex)

        @argument_codex.deleter
        def argument_codex(self):
            self.__argument_name_table.clear()

        arguments = args = argument_codex

        @property
        def argument_converters(self) -> "dict[str, Callable[[Any], Any]]":
            """
            The converter table for the arguments of this call.
            """
            return {arg_name : Translator.ARGUMENT_CONVERTERS[arg_converter] for arg_name, arg_converter in self.__argument_converters.items()}
        
        @argument_converters.setter
        def argument_converters(self, codex : dict[str, "Translator.FUNC_NAMES"]):
            if isinstance(codex, dict):
                try:
                    codex = Translator.StrDict(codex)
                except:
                    raise TypeError("Expected dict with str keys and str values")
            if not isinstance(codex, Translator.StrDict):
                raise TypeError(f"Expected dict, got '{type(codex).__name__}'")
            for conv in codex.values():
                if conv not in Translator.ARGUMENT_CONVERTERS:
                    raise ValueError(f"Expected valid converter names, got '{conv}'")
            self.__argument_converters.clear()
            self.__argument_converters.update(codex)

        @argument_converters.deleter
        def argument_converters(self):
            self.__argument_converters.clear()

        converters = conv = argument_converters



    def __init__(self) -> None:
        self.__original_names : "dict[str, str]" = {}
        self.__argument_names_translation_table : "dict[str, Translator.StrDict]" = {}
        self.__argument_converter_table : "dict[str, Translator.StrDict]" = {}
        self.__translation_table : dict = {
            "Names" : self.__original_names,
            "Argument Name Translations" : self.__argument_names_translation_table,
            "Argument Converters" : self.__argument_converter_table
        }
    
    def export_to_file(self, path : Path | str):
        """
        Exports the Translator to the given file path as a JSON.
        """
        if isinstance(path, str):
            try:
                path = Translator.__Path(path)
            except:
                pass
        if not isinstance(path, Translator.__Path):
            raise TypeError(f"Expected Path, got '{type(path).__name__}'")
        with path.open("w") as file:
            Translator.__json.dump(self.__translation_table, file, indent = "\t")
        
    @staticmethod
    def import_from_file(path : Path | str) -> "Translator":
        """
        Returns a Translator built from the given JSON file.
        """
        from pathlib import Path
        import json
        if isinstance(path, str):
            try:
                path = Path(path)
            except:
                pass
        if not isinstance(path, Path):
            raise TypeError(f"Expected Path, got '{type(path).__name__}'")
        with path.open("r") as file:
            try:
                self = Translator()
                self.__translation_table = json.load(file)
                self.__original_names = self.__translation_table.setdefault("Names", {})
                self.__argument_names_translation_table = self.__translation_table.setdefault("Argument Name Translations", {})
                self.__argument_converter_table = self.__translation_table.setdefault("Argument Converters", {})
            except json.JSONDecodeError:
                raise ValueError(f"Given path is not a JSON file or is corrupted: '{path}'")
        return self
    
    @property
    def names(self) -> list[str]:
        """
        Returns the list of API call names translated by this Translator.
        """
        return list(self.__original_names.values())
    
    def __getitem__(self, name : str) -> "Translator.CallTranslation":
        """
        Implements self[name]. Returns the translation of the call with the given name.
        """
        if not isinstance(name, str):
            raise TypeError(f"Expected str, got '{type(name).__name__}'")        
        return Translator.CallTranslation(self, self.__original_names.setdefault(name.lower(), name), self.__argument_names_translation_table.setdefault(name.lower(), Translator.StrDict()), self.__argument_converter_table.setdefault(name.lower(), Translator.StrDict()))
    
    def __contains__(self, name : str) -> bool:
        """
        Implements name in self.
        """
        if not isinstance(name, str):
            raise TypeError(f"Expected str, got '{type(name).__name__}'")
        return name.lower() in self.__original_names

    def translate(self, c : "CallInfo") -> "CallInfo":
        """
        Translates the given API call. Modifies the CallInfo object directly and returns it.
        """
        if c.API in self:
            translation = self[c.API]
            try:
                c.arguments = {(translation.args[name] if name in translation.args else name) : (translation.conv[name](value) if name in translation.conv else value) for name, value in c.arguments.items()}
            except:
                raise
            c.flags = {(translation.args[name] if name in translation.args else name) : value for name, value in c.flags.items()} 
        return c
    
    def __call__(self, c : "CallInfo") -> "CallInfo":
        return self.translate(c)




class MissingBehavioralInfoError(ValueError):
    
    """
    This exception indicates that the input report does not contain the necessary behavioral monitoring information.
    """

class MissingSamplePathError(ValueError):

    """
    This exception signals that the sample path in the test machine could not be found.
    """





del Callable, Iterable, Path, Any, Literal