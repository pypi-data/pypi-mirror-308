"""
This module holds the tools to create progress bars for the different BAGUETTE tools.
"""

from types import TracebackType

__all__ = ["ProgressBar"]





class ProgressBar:

    """
    A wrapper class for alive_progress.alive_bar to make it more flexible.
    """

    from alive_progress import alive_bar
    __alive_bar = staticmethod(alive_bar)
    del alive_bar

    def __init__(self, title : str) -> None:
        if not isinstance(title, str):
            raise TypeError(f"Expected str, got '{type(title).__name__}'")
        self.__total = None
        self.__current = None
        self.__progress = 0.0
        self.__bar = None
        self.__bar_context = ProgressBar.__alive_bar(manual = True, monitor = False, title = title, stats = "| {eta} |") # , length = ProgressBar.__get_terminal_size()[0]

    @property
    def total(self) -> int | None:
        """
        The total amount of elements in the current task.
        """
        return self.__total
    
    @total.setter
    def total(self, total : int):
        if not isinstance(total, int):
            raise TypeError(f"Expected int, got '{type(total).__name__}'")
        if total <= 0:
            raise ValueError(f"Expected nonzero positive integer, got {total}")
        self.__total = total
        if self.__current is None:
            self.__current = round(self.__progress * self.__total)
        else:
            self.__progress = self.__current / self.__total
        if self.__bar is not None:
            self.__bar.text(f"{self.__current}/{total}") # type: ignore
            self.__bar(self.__progress)
    
    @total.deleter
    def total(self):
        self.__total = None
        self.__current = None
        if self.__bar is not None:
            self.__bar.text() # type: ignore

    @property
    def progress(self) -> float:
        """
        The current progress of the task (float between 0 and 1).
        """
        return self.__progress
    
    @progress.setter
    def progress(self, progress : float):
        if not isinstance(progress, float):
            raise TypeError(f"Expected float, got '{type(progress).__name__}'")
        if not 0 <= progress <= 1:
            raise ValueError(f"Expected value between zero and one, got {progress}")
        self.__progress = progress
        if self.__total is not None:
            self.__current = round(self.__progress * self.__total)
            if self.__bar is not None:
                self.__bar.text(f"{self.__current}/{self.__total}") # type: ignore
        if self.__bar is not None:
            self.__bar(self.__progress)

    @property
    def current(self) -> int:
        """
        The current progress if total is set.
        """
        if self.__current is None:
            raise RuntimeError("No total value set for progress bar")
        return self.__current
    
    @current.setter
    def current(self, current : int):
        if not isinstance(current, int):
            raise TypeError(f"Expected int, got '{type(current).__name__}'")
        if self.__total is None:
            self.__total = round(current / self.__progress)
        if not 0 <= current <= self.__total:
            raise ValueError(f"Expected value between 0 and {self.__total}, got {current}")
        self.__current = current
        self.__progress = self.__current / self.__total
        if self.__bar is not None:
            self.__bar.text(f"{self.__current}/{self.__total}") # type: ignore
            self.__bar(self.__progress)

    def __enter__(self):
        self.__bar = self.__bar_context.__enter__()
        if self.__total is not None and self.__current is not None:
            self.__bar.text(f"{self.__current}/{self.__total}") # type: ignore
        self.__bar(self.__progress)
        return self
    
    def __exit__[E : BaseException](self, exc_type : type[E] | None = None, exc : E | None = None, traceback : TracebackType | None = None):
        if self.__bar is None:
            raise RuntimeError("__exit__ called without a call to __enter__")
        self.__bar_context.__exit__(exc_type, exc, traceback)





del TracebackType