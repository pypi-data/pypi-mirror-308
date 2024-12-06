from typing import Any, Dict, Iterable, Union
from Viper.frozendict import frozendict





class Record(frozendict[str, int | float | bool | bytes | str]):

    """
    A subclass of frozendict to hold key-values informations with str keys.
    They can be used with attributes too.
    """

    KEY_ERROR_MESSAGE = "KeyError: {key}"
    ATTRIBUTE_ERROR_MESSAGE = "'{cls}' object has not attribute '{key}'"
    data : dict[str, Any] = {}



    class RecordKeyError(KeyError):

        def __init__(self, message : str, data : dict[str, Any] | None = None) -> None:
            super().__init__(message)
            self.data = data

    class RecordAttributeError(AttributeError):

        def __init__(self, message : str, data : dict[str, Any] | None = None) -> None:
            super().__init__(message)
            self.data = data



    def __getitem__(self, k: str) -> int | float | bool | bytes | str:
        if not isinstance(k, str):
            raise TypeError(f"Record keys must be str, not '{type(k).__name__}'")
        try:
            return super().__getitem__(k)
        except KeyError:
            raise Record.RecordKeyError(type(self).KEY_ERROR_MESSAGE.format(key = k, **self.data), self.data if self.data is not type(self).data else None) from None
    
    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError as e:
            try:
                return self[name]
            except KeyError:
                raise Record.RecordAttributeError(type(self).ATTRIBUTE_ERROR_MESSAGE.format(key = name, cls = type(self).__name__, **self.data), self.data if self.data is not type(self).data else None) from None
    
    def __delattr__(self, name: str) -> None:
        if name in super().__getattribute__("__dict__"):
            raise ValueError("Cannot delete attribute '{}' for this object.".format(name))
        try:
            self.pop(name)
        except KeyError as e:
            raise Record.RecordAttributeError(type(self).ATTRIBUTE_ERROR_MESSAGE.format(key = name, cls = type(self).__name__, **self.data), self.data if self.data is not type(self).data else None) from None
    
    def __dir__(self) -> list[str]:
        return list(super().__dir__()) + list(self.keys())

    



del Any, Dict, Iterable, Union, frozendict