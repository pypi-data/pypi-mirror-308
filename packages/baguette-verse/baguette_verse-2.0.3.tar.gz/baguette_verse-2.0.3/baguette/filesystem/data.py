"""
This data defines a readable and writable dict-like data structure for storing random information to a BAGUETTE file.
"""

from typing import Any, Callable, Iterable

__all__ = ["Data"]





class Data:

    """
    A dict-like class that only holds static data (json-serializable and not hashable), that updates BAGUETTE files upon modification and that works by attribute access:

    >>> d = Data()
    >>> d.hello = "Hello World!"
    >>> d.hello
    'Hello World!'
    >>> d.goodbye = []
    >>> d.goodbye       # List are not hashable and are replaced by tuples if hashable.
    ()
    >>> d.goodbye = [[]]        # That's too much.
    TypeError: Expected hashable, got 'list'
    >>> d.goodbye = {"a" : 1}
    >>> d.goodbye       # Dicts are replaced by Data if hashable.
    Data(a = 1)
    >>> d.goodbye.a
    1
    >>> del d.goodbye
    >>> d
    Data(hello = 'Hello World!')
    """
    
    __slots__ = {
        "__updater" : "An updater function (of a BaguetteFile object) to signal modifications",
        "__dict" : "The actual dictionnary containing the different fields"
    }

    from typing import Hashable as __Hashable
    from json import dumps as __dumps
    __dumps = staticmethod(__dumps)

    def __init__(self, updater : Callable[[], None] | None = None, /, **kwargs) -> None:
        if updater is not None and not callable(updater):
            raise TypeError(f"Expected callable or None for updater, got '{type(updater).__name__}'")
        self.__dict : "dict[str, Any]" = {}
        self.__updater = None
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.__updater = updater
    
    def dump(self) -> dict[str, Any]:
        """
        Returns a dict version of self.
        """
        return {name : value for name, value in self.items()}
    
    def __formatter(self, value):
        """
        Internal function to check that the value can be used in a Data record.
        Changes the value if possible and returns the new one.
        """
        t = type(value)
        if isinstance(value, list):
            value = tuple(value)
        if isinstance(value, set):
            value = frozenset(value)
        if isinstance(value, dict):
            value = Data(**value)
        if not isinstance(value, Data):
            if not isinstance(value, Data.__Hashable):
                raise TypeError(f"Expected hashable, got '{t.__name__}'")
            try:
                hash(value)
            except:
                raise TypeError(f"Expected hashable, got '{t.__name__}'")
        try:
            def fix_data(obj):
                if isinstance(obj, Data):
                    return obj.dump()
                return obj
            Data.__dumps(self, default=fix_data)
        except:
            raise TypeError(f"Object is not json-serializable: {self}")
        return value

    def __setter(self, name : str, value : Any):
        """
        Internal function used to set the value associated with a field.
        """
        value = self.__formatter(value)
        self.__dict[name] = value
        if isinstance(value, Data):
            value.__updater = self.__updater

        if self.__updater is not None:
            self.__updater()

    def __deleter(self, name : str):
        """
        Internal function used to delete the value associated with a field.
        """
        self.__dict.pop(name)
        if self.__updater is not None:
            self.__updater()

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            if name in ("_Data__dict", "_Data__updater"):
                return super().__getattribute__(name)
            if name in self.__dict:
                return self.__dict[name]
            raise
    
    def __setattr__(self, name: str, value: Any) -> None:
        try:
            super().__getattribute__(name)
        except AttributeError:
            if name in ("_Data__dict", "_Data__updater"):
                return super().__setattr__(name, value)
            self.__setter(name, value)
            return 
        super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        try:
            super().__getattribute__(name)
        except AttributeError:
            if name in ("_Data__dict", "_Data__updater"):
                return super().__delattr__(name)
            if name not in self.__dict:
                raise
            self.__deleter(name)
            return 
        super().__delattr__(name)

    def __dir__(self) -> Iterable[str]:
        yield from self.__dict
        yield from super().__dir__()
    
    def __iter__(self) -> Iterable[str]:
        yield from self.__dict
    
    def keys(self):
        return self.__dict.keys()
    
    def values(self):
        return self.__dict.values()
    
    def items(self):
        return self.__dict.items()
    
    def __str__(self) -> str:
        return "{" + ", ".join(f"{name} : {value}" for name, value in self.items()) + "}"
    
    def __repr__(self) -> str:
        return "Data(" + ", ".join(f"{name} = {repr(value)}" for name, value in self.items()) + ")"
    
    def __bool__(self) -> bool:
        return len(self.__dict) > 0
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Data):
            return False
        return self.__dict == value.__dict
    




del Iterable, Any, Callable