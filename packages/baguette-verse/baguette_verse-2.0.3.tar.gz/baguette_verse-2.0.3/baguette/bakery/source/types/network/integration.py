"""
This module contains integration protocols for this behavioral package.
"""

from .....logger import logger
from ...utils import chrono
from ..execution.entities import Call
from ..execution.utils import CallHandler
from . import entities, relations
from Viper.collections.isomorph import IsoDict
__all__ = []





logger.info("Loading integrations from {} library.".format(__name__.rpartition(".")[0].rpartition(".")[2]))

__active_connections : IsoDict[entities.Socket, entities.Connection] = IsoDict()
__active_handles : IsoDict[entities.Socket, int] = IsoDict()
__inverted_handles : IsoDict[int, entities.Socket] = IsoDict()

@chrono
def integrate_socket_creation(c : Call):
    """
    Creates a Socket vertex and links it to the call that created it.
    """
    from .....logger import logger
    from .entities import Socket
    from .relations import CreatesSocket, HasSocket
    if c.status == 1:
        logger.debug("Socket created.")
        s = Socket(
            handle = c.arguments.socket,
            family = Socket.families[c.arguments.af][0],
            protocol = Socket.protocols[c.arguments.protocol][0],
            type = Socket.types[c.arguments.type][0]
            )
        __active_handles[s] = c.arguments.socket
        __inverted_handles[c.arguments.socket] = s
        if s in __active_connections:
            __active_connections.pop(s)
        CreatesSocket(c, s)
        HasSocket(c.thread.process, s)

@chrono
def integrate_socket_binding(c : Call):
    """
    Creates a Connection vertex and binds it to a local address.
    """
    from .....logger import logger
    from ...utils import active_builder
    from .entities import Connection
    from .relations import Binds, Communicates, HasConnection
    if c.status == 1:
        logger.debug("Socket bound.")
        l = Connection()
        if c.arguments.socket in __inverted_handles:
            s = __inverted_handles[c.arguments.socket]
        else:
            logger.warning("Binding to non-existing socket.")
            return
        __active_connections[s] = l
        HasConnection(s, l)
        builder = active_builder()
        if builder is None:
            raise RuntimeError("Integration functions called outside of a buidling cycle!")
        Communicates(l, builder.host)
        if s.family == "InterNetwork":
            b = Binds(c, l, src = (c.arguments.ip_address, c.arguments.port))
            l.src = b.src
        else:
            b = Binds(c, l, src = ("Unknown", -1))
            logger.error("I don't know how to handle this type of address:\n{}".format(s))

@chrono
def integrate_socket_connection(c : Call):
    """
    Sets the remote address of a connection.
    """
    from .....logger import logger
    from ...utils import active_builder
    from .entities import Connection, Host
    from .relations import Communicates, Connects, HasConnection
    if c.status == 1:
        logger.debug("Socket connected.")
        try:
            sock = c.arguments.socket
        except AttributeError:
            sock = c.arguments.s
        if sock in __inverted_handles:
            s = __inverted_handles[sock]
        else:
            logger.warning("Connecting from non-existing socket.")
            return
        if s in __active_connections:
            l = __active_connections[s]
            logger.warning("Trying to connect an unbound socket...")
        else:
            l = Connection()
        HasConnection(s, l)
        builder = active_builder()
        if builder is None:
            raise RuntimeError("Integration functions called outside of a buidling cycle!")
        Communicates(l, builder.host)
        __active_connections[s] = l
        for dest in Host:
            if dest.address == c.arguments.ip_address:
                break
        else:
            dest = Host(address = c.arguments.ip_address, name = "", domain = "", platform = "")
        Communicates(l, dest)
        if s.family == "InterNetwork":
            b = Connects(c, l, dst = (c.arguments.ip_address, c.arguments.port))
            l.dst = b.dst
        else:
            b = Connects(c, l, dst = ("Unknown", -1))
            logger.error("I don't know how to handle this type of address:\n{}".format(s))


@chrono
def integrate_socket_listening(c : Call):
    """
    Sets the socket in listening mode.
    """
    from .....logger import logger
    from .relations import ListensOn
    if c.status == 1:
        logger.debug("Socket listening.")
        if c.arguments.socket in __inverted_handles:
            s = __inverted_handles[c.arguments.socket]
        else:
            logger.warning("Listening from non-existing socket.")
            return
        ListensOn(c, s)

@chrono
def integrate_socket_accepting(c : Call):
    """
    Sets a connection remote address through an accept system call. Also creates a new socket object.
    """
    from .....logger import logger
    from .entities import Connection, Host, Socket
    from .relations import Accepts, Communicates, Duplicates, HasConnection
    if c.status == 1:
        logger.debug("Socket accepting connection.")
        if c.arguments.socket in __inverted_handles:
            s = __inverted_handles[c.arguments.socket]
        else:
            logger.warning("Accepting from non-existing socket.")
            return
        s1 = Socket(handle = c.return_value, family = s.family, protocol = s.protocol, type = s.type)
        l1 = Connection()
        __active_handles[s1] = c.return_value
        __inverted_handles[c.return_value] = s1
        if s not in __active_connections:
            logger.warning("Accepting from unbound socket...")
        else:
            l = __active_connections[s]
            l1.src = l.src
        HasConnection(s1, l1)
        Duplicates(s, s1)
        for dest in Host:
            if dest.address == c.arguments.ip_address:
                break
        else:
            dest = Host(address = c.arguments.ip_address, name = "", domain = "", platform = "")
        Communicates(l1, dest)
        if s1.family == "InterNetwork":
            b = Accepts(c, l1, dst = (c.arguments.ip_address, c.arguments.port))
            l1.dst = b.dst
        else:
            b = Accepts(c, l1, dst = ("Unknown", -1))
            logger.error("I don't know how to handle this type of address:\n{}".format(s))

@chrono
def integrate_socket_close(c : Call):
    """
    Closes a socket and the connection linked to it.
    """
    from .....logger import logger
    from .relations import Closes, CloseSocket
    if c.status == 1:
        logger.debug("Closing socket.")
        if c.arguments.socket in __inverted_handles:
            s = __inverted_handles[c.arguments.socket]
        else:
            logger.warning("Closing non-existing socket.")
            return
        CloseSocket(c, s)
        handle = __active_handles.pop(s)
        __inverted_handles.pop(handle)
        if s in __active_connections:
            l = __active_connections.pop(s)
            Closes(c, l)
        else:
            logger.warning("Closing down unbound socket...")

@chrono
def integrate_socket_shutdown(c : Call):
    """
    Closes a connection.
    """
    from .....logger import logger
    from .relations import Shutdown
    if c.status == 1:
        logger.debug("Closing socket.")
        if c.arguments.socket in __inverted_handles:
            s = __inverted_handles[c.arguments.socket]
        else:
            logger.warning("Shuting down non-existing socket")
            return
        if s in __active_connections:
            l = __active_connections.pop(s)
            Shutdown(c, l)
        else:
            logger.warning("Shuting down unbound socket...")

@chrono
def integrate_socket_send(c : Call):
    """
    Sends data through a connection.
    """
    from .....logger import logger
    from ..data import Data
    from ..data.integration import register_write_operation
    from .relations import Conveys, Sends
    if c.status == 1:
        logger.debug("Sending data.")
        if c.arguments.socket in __inverted_handles:
            s = __inverted_handles[c.arguments.socket]
        else:
            logger.warning("Sending through non-existing socket.")
            return
        if s not in __active_connections:
            logger.warning("Sending through unbound socket.")
        else:
            l = __active_connections[s]
            d = Data(time = c.time, data = c.arguments.buffer.encode())
            Sends(c, d)
            Conveys(d, l)
            l.volume += len(d.data)
            register_write_operation(l, s, c.arguments.buffer)

@chrono
def integrate_socket_recv(c : Call):
    """
    Receives data through a connection.
    """
    from .....logger import logger
    from ..data import Data
    from ..data.integration import register_read_operation
    from .relations import Conveys, Receives
    if c.status == 1:
        logger.debug("Receiving data.")
        if c.arguments.socket in __inverted_handles:
            s = __inverted_handles[c.arguments.socket]
        else:
            logger.warning("Receiving through non-existing socket.")
            return
        if s not in __active_connections:
            logger.warning("Receiving through unbound socket.")
        else:
            l = __active_connections[s]
            d = Data(time = c.time, data = c.arguments.buffer.encode())
            Receives(d, c)
            Conveys(l, d)
            l.volume += len(d.data)
            register_read_operation(l, s, c.arguments.buffer)





# Socket creation
CallHandler(integrate_socket_creation, "socket", "WSASocketW")

# Socket binding
CallHandler(integrate_socket_binding, "bind")

# Socket connecting
CallHandler(integrate_socket_connection, "connect", "WSAConnect")

# Socket listening
CallHandler(integrate_socket_listening, "listen")

# Socket accepting
CallHandler(integrate_socket_accepting, "accept")

# Socket closing
CallHandler(integrate_socket_close, "closesocket")

# Socket shuting down
CallHandler(integrate_socket_shutdown, "shutdown")

# Socket sending
CallHandler(integrate_socket_send, "send")

# Socket receiving
CallHandler(integrate_socket_recv, "recv")





del Call, CallHandler, IsoDict, chrono, entities, integrate_socket_accepting, integrate_socket_binding, integrate_socket_close, integrate_socket_connection, integrate_socket_creation, integrate_socket_listening, integrate_socket_recv, integrate_socket_send, integrate_socket_shutdown, logger, relations