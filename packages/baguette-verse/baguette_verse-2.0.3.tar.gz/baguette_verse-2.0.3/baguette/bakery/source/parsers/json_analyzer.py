"""
This module adds a JSON parsing system that learns the json structure of a certain type of files given multiple examples.
"""

from abc import ABCMeta, abstractmethod
from typing import Any, Iterable, Iterator, overload





type JSONObject = int | float | bool | None | str | list[JSONObject] | dict[str, JSONObject]

class JSONNode[X : JSONObject](metaclass = ABCMeta):

    """
    An abstract node to learn the type of a given JSON entry.
    """

    type cls_dict[T : JSONObject] = "dict[type[T], type[JSONNode[T]]]"
    classes : cls_dict = {}

    @overload
    @abstractmethod
    def update(self, entry : X) -> "JSONNode[X]":
        pass

    @overload
    @abstractmethod
    def update[Y : JSONObject](self, entry : Y) -> "JSONNode[Y]":
        pass

    @abstractmethod
    def update(self, entry):
        """
        Updates the knwoledge of the given node given a new example. Returns the new appropriate node.
        """
        raise NotImplementedError
    
    @abstractmethod
    def dump(self, indent : int = 0) -> str:
        """
        Returns a string that represents the learned syntax.
        """
        raise NotImplementedError
            
    @staticmethod
    def get_adequate_node[T : JSONObject](entry : T) -> "JSONNode[T]":
        """
        Returns the adequate node for given type.
        """
        return JSONNode.classes.get(type(entry), AnyNode)().update(entry)





class AnyNode(JSONNode[Any]):

    """
    This node means no useful type hint could be learned.
    """

    def update(self, entry):
        return self
    
    def dump(self, indent : int = 0) -> str:
        return "Any"
    




class StrNode(JSONNode[str]):

    """
    This node means the current node is always a string.
    """

    def update(self, entry):
        if isinstance(entry, str):
            return self
        else:
            return AnyNode()
        
    def dump(self, indent : int = 0) -> str:
        return "str"
        




class IntNode(JSONNode[int]):

    """
    This node means the current node is always an integer.
    """

    def update(self, entry):
        if isinstance(entry, int):
            return self
        else:
            return AnyNode()
        
    def dump(self, indent : int = 0) -> str:
        return "int"
        




class FloatNode(JSONNode[float]):

    """
    This node means the current node is always a float.
    """

    def update(self, entry):
        if isinstance(entry, float):
            return self
        else:
            return AnyNode()

    def dump(self, indent : int = 0) -> str:
        return "float"
        




class BoolNode(JSONNode[bool]):

    """
    This node means the current node is always a boolean.
    """

    def update(self, entry):
        if isinstance(entry, bool):
            return self
        else:
            return AnyNode()
        
    def dump(self, indent : int = 0) -> str:
        return "bool"
        




class NullNode(JSONNode[None]):

    """
    This node means the current node is always None.
    """

    def update(self, entry):
        if entry is None:
            return self
        else:
            return AnyNode()
        
    def dump(self, indent : int = 0) -> str:
        return "None"





class ArrayNode(JSONNode[list]):

    """
    This node means the current node is always a list of a certain type.
    """

    def __init__(self) -> None:
        self.type : "JSONNode | None" = None

    def update(self, entry):
        if not isinstance(entry, list):
            return AnyNode()
        for e in entry:
            if self.type is None:
                self.type = JSONNode.get_adequate_node(e)
            else:
                self.type = self.type.update(e)
        return self
    
    def dump(self, indent : int = 0) -> str:
        if self.type is None or isinstance(self.type, AnyNode):
            return "list"
        else:
            return f"list[{self.type.dump(indent)}]"





class ObjectNode(JSONNode[dict]):

    """
    This node means that the current node is always a typed dictionary.
    """

    COMPACTION_SIZE = 15

    def __init__(self) -> None:
        self.entries : "dict[str, JSONNode] | None" = None
        self.always : "dict[str, bool]" = {}

    def update(self, entry):
        if not isinstance(entry, dict):
            return AnyNode()
        if self.entries is None:
            self.entries = {}
            for k, v in entry.items():
                if not isinstance(k, str):
                    raise TypeError(f"Got a non-str key in json object: {k}")
                self.entries[k] = JSONNode.get_adequate_node(v)
                self.always[k] = True
        else:
            unseen : "set[str]" = set(self.entries)
            for k, v in entry.items():
                if not isinstance(k, str):
                    raise TypeError(f"Got a non-str key in json object: {k}")
                if k not in self.entries:
                    self.entries[k] = JSONNode.get_adequate_node(v)
                    self.always[k] = False
                else:
                    self.entries[k] = self.entries[k].update(v)
                    unseen.remove(k)
            for k in unseen:
                self.always[k] = False
        return self

    def dump(self, indent : int = 0) -> str:
        if self.entries is None or all((e is None or isinstance(e, AnyNode)) for e in self.entries.values()):
            return "dict"
        elif len(self.entries) > ObjectNode.COMPACTION_SIZE and len(set((t := e.dump(indent + 1)) for e in self.entries.values())) == 1:
            return f"dict[str, {t}]"
        elif len(self.entries) > ObjectNode.COMPACTION_SIZE:
            return "dict"
        else:
            s = "{\n"
            for k, v in self.entries.items():
                if self.always[k]:
                    s += "\t" * (indent + 1) + f"'{k}' : {v.dump(indent + 1)},\n"
                else:
                    s += "\t" * (indent + 1) + f"'{k}' : NotRequired[{v.dump(indent + 1)}],\n"
            s += "\t" * indent + "}"
            return s
        




JSONNode.classes.update({
    Any : AnyNode,
    str : StrNode,
    int : IntNode,
    float : FloatNode,
    bool : BoolNode,
    type(None) : NullNode,
    list : ArrayNode,
    dict : ObjectNode
})





def learn_syntax[T : JSONObject](g : Iterable[T]) -> Iterator[JSONNode[T]]:
    """
    Given an iterable of JSON-like objects, returns the learned grammar of these objects.
    """
    g = iter(g)
    try:
        first = next(g)
    except StopIteration:
        print("Not even a first element")
        yield AnyNode()
        return
    node = JSONNode.get_adequate_node(first)
    print(f"First element is a {type(node).__name__}")
    yield node
    for e in g:
        node = node.update(e)
        yield node





del ABCMeta, abstractmethod, Any, Iterable, Iterator, overload