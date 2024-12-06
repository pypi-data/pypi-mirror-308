"""
The event library. An event can be created by anyone, specifying any kind of data. Anybody can wait for any type of events.
Look at the Event class.
"""

from typing import Callable, Self, TypeVar
from Boa.parallel.thread import Future
from threading import Lock

__all__ = ["Event"]





class Event:

    """
    The base event class. Use its static methods to react to Events created.
    To wait for an event of a specific event class, just use:
    >>> cls.wait()      # Returns the cls instance that was thrown.
    To throw an event, use:
    >>> event = cls()
    >>> event.throw()

    The event system works with class hierarchy:
    >>> class MyEvent(Event):
    ...     pass
    ... 
    >>> MyEvent.wait()  # Only waits for events that satisfy isinstance(event, MyEvent).
    >>> Event.wait()    # Waits for any kind of event.
    """

    __waiting : set[Future[Self]] = set()
    __callbacks : list[Callable[[Self], None]] = []
    __lock : Lock = Lock()

    __slots__ = {}

    def __str__(self) -> str:
        """
        Implements str(self).
        """
        return type(self).__name__ + "(" + ", ".join(str(name) + " = " + repr(getattr(self, name)) for name in self.__slots__) + ")"

    def throw(self) -> bool:
        """
        Triggers the Event. Everyone waiting for it will be awaken, and corresponding callbacks will be called.
        Returns True if anybody reacted to the event. Returns False otherwise.
        """
        from ...logger import logger

        def raise_multiple_exceptions(exceptions : list[BaseException]):
            """
            Raises all the exceptions in the given list, in order.
            """
            if not exceptions:
                return
            try:
                raise exceptions.pop() from None
            finally:
                raise_multiple_exceptions(exceptions)

        classes : "set[type[Event]]" = {type(self)}
        done : "set[type[Event]]" = set()
        ok = False
        logger.debug("Throwing {}.".format(self))
        while classes:
            cls = classes.pop()

            with cls.__lock:

                for fut in cls.__waiting:
                    fut.set(self)
                    ok = True
                cls.__waiting.clear()
                
                exceptions : list[BaseException] = []
                for cb in cls.__callbacks:
                    try:
                        cb(self)
                        ok = True
                    except BaseException as e:
                        exceptions.append(e)
                raise_multiple_exceptions(exceptions)

            done.add(cls)
            classes.update(c for c in cls.__bases__ if issubclass(c, Event))
            classes.difference_update(done)
        
        return ok

    @classmethod
    def __init_subclass__(cls) -> None:
        from threading import Lock
        cls.__lock = Lock()
        cls.__callbacks = []
        cls.__waiting = set()

    @classmethod
    def wait(cls : type[Self]) -> Self:
        """
        Waits for an Event of this class or of any subclasses to occur. Returns the Event object when it happens.
        """
        from Boa.parallel.thread import Future
        fut : "Future[Self]" = Future()
        with cls.__lock:
            cls.__waiting.add(fut)
        return fut.result()
    
    @classmethod
    def add_callback(cls : type[Self], callback : Callable[[Self], None]):
        """
        Adds a callback to be performed after a realization of an event of this class or of any of its subclasses. The callback will persist until it is removed.
        """
        with cls.__lock:
            cls.__callbacks.append(callback)
    
    @classmethod
    def remove_callback(cls : type[Self], callback : Callable[[Self], None]) -> bool:
        """
        Removes a callback to be performed after a realization of an event with the given name. Returns True if a callback was indeed deleted.
        """
        with cls.__lock:
            try:
                cls.__callbacks.remove(callback)
                return True
            except ValueError:
                return False





Event.__init_subclass__()       # It must initialize itself, as if it was one of its own subclasses.

del Callable, Future, Lock