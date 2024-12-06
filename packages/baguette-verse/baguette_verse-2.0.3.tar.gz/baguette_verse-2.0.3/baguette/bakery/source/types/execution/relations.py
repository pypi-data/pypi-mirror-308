"""
This module contains Edge and Arrow subclasses for this behavioral package.
"""

from .....logger import logger
from ...config import SwitchSetting
from ...colors import Color
from ...graph import Arrow, DataEdge, Edge, Vertex
from ..filesystem.entities import Directory, File
from .entities import Call, Process, Thread

__all__ = ["HasChildProcess", "UsesAsArgument", "Runs", "HasThread", "HasFirstCall", "FollowedBy", "NextSignificantCall", "StartedThread", "InjectedThread", "StartedProcess"]





logger.info("Loading relations from {} library.".format(__name__.rpartition(".")[0].rpartition(".")[2]))

class HasChildProcess(Arrow):

    """
    This kind of arrow indicates that a process created another one.
    """

    source : Process
    destination : Process





class UsesAsArgument(Edge):

    """
    This kind of edge indicates that a process used a file or directory in its command line.
    """

    source : Process
    destination : File | Directory




class Runs(Edge):
    
    """
    This kind of edge indicates process ran a file as its program.
    """

    source : Process
    destination : File





class HasThread(Edge):

    """
    This kind of edge indicates that a process hosts a thread.
    """

    label : str = ""

    source : Process
    destination : Thread





class HasFirstCall(Edge):

    """
    This kind of edge indicates what was the first system call of a thread.
    """

    label : str = ""

    source : Thread
    destination : Call





class FollowedBy(Arrow):

    """
    This kind of arrow indicates that a system call was followed by another one.
    """

    label : str = ""

    source : Call
    destination : Call





class NextSignificantCall(Arrow):
    
    """
    This kind of arrows links two Call nodes that happened one after the other in the same thread both nodes are linked to other types of nodes.
    """

    label : str = ""

    source : Call
    destination : Call





class StartedThread(DataEdge):

    """
    This kind of edge indicates that a system call started a new thread.
    """

    __slots__ = {
        "__remote" : "Indicates if the started thread was started in another process (remote thread)"
    }

    __defining_data__ = DataEdge.__defining_data__ | {
        "remote"
    }

    label : str = ""

    source : Call
    destination : Thread

    def __init__(self, source: Vertex, destination: Vertex, *, auto_write: bool = True, remote : bool) -> None:
        super().__init__(source, destination, auto_write = auto_write, remote = remote)

    @property
    def remote(self) -> bool:
        """
        Indicates if this the started Thread belongs to a different Process than the one that started it.
        """
        return self.__remote
    
    @remote.setter
    def remote(self, r : bool):
        if not isinstance(r, bool):
            raise TypeError(f"Expected bool, got '{type(r).__name__}'")
        self.__remote = r
    




class InjectedThread(Arrow):

    """
    This kind of arrow indicates a process created a remote thread.
    """

    source : Process
    destination : Thread





class StartedProcess(Edge):

    """
    This kind of edge indicates that a system call started a new process.
    """

    label : str = ""

    source : Call
    destination : Process





del Arrow, DataEdge, Call, Color, SwitchSetting, Directory, Edge, File, Process, Thread, Vertex, logger