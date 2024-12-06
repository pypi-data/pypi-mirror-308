"""
This file defines the BAGUETTE error codes. These are the exit code returned by BAGUETTE programs and are mapped to specific exceptions.
When creating new exceptions that should cause a crash, remember to create an exit code and the corresponding checker.
"""

from argparse import ArgumentParser
from enum import IntFlag, auto, nonmember
from typing import Any, NoReturn, Protocol
from traceback import format_exc, format_exception
from sys import exception
from .logger import logger

__all__ = ["ExitCode", "ExitCodeParser"]





class KeywordChecker(Protocol):

    """
    A typing class for checker callbacks that accepts any keyword arguments (with a **kwarg).
    """

    def __call__(self, exc : BaseException | None, **kwargs: Any) -> bool:
        raise NotImplementedError





handler_dict : "dict[ExitCode, KeywordChecker]" = {}

class ExitCode(IntFlag):

    EXIT_CODE_MATCHING_EXCEPTION = auto()
    UNKNOWN_EXCEPTION = auto()
    KEYBOARD_INTERRUPT = auto()
    BAGUETTE_FORMAT_ERROR = auto()
    ONTOLOGICAL_WARNING = auto()
    PARSING_ERROR = auto()
    PREPARING_EXCEPTION = auto()
    BAKING_TIMEOUT = auto()
    BAKING_UNKNOWN_EXCEPTION = auto()
    BAKING_MISSING_DATA = auto()
    TOASTING_UNKNOWN_EXCEPTION = auto()
    TOASTING_TIMEOUT = auto()
    OPENING_GEPHI_RUNTIME_ERROR = auto()
    OPENING_GEPHI_STARTING_ERROR = auto()

    __handlers = handler_dict
    __exception = staticmethod(exception)
    __format_exc = staticmethod(format_exc)
    __format_exception = staticmethod(format_exception)
    __logger = logger

    def register_error_code_checker(self, checker : KeywordChecker):
        """
        Associates an error code with a context checker function:
        When about to exit, a BAGUETTE program will run this function to check if the return code should contain the flag.
        """
        ExitCode.__handlers[self] = checker
        ExitCode.__logger.debug(f"Registered handler {checker} for exit code {self}")

    @staticmethod
    def exit(*flags: "ExitCode", **kwargs : Any) -> NoReturn:
        """
        Returns the most appropriate exit code given the current context.
        All arguments are passed to the checkers.
        """
        exc = ExitCode.__exception()
        flag = ExitCode(0)
        try:
            for f in flags:
                if not isinstance(f, ExitCode):
                    raise TypeError(f"Expected ExitCode, got '{type(f).__name__}'")
                flag |= f
            for code, checker in ExitCode.__handlers.items():
                if checker(exc, **kwargs):
                    flag |= code
            if exc is not None and not flag:
                ExitCode.__logger.error(f"Unknown BAGUETTE exception could not be handled:\n{ExitCode.__format_exception(exc)}") # type: ignore
                ExitCode.__logger.info(f"Exiting with exit code {ExitCode.UNKNOWN_EXCEPTION}")
                exit(ExitCode.UNKNOWN_EXCEPTION)
            ExitCode.__logger.info(f"Exiting with exit code {flag}")
            exit(flag)
        except SystemExit:
            raise
        except:
            ExitCode.__logger.error(f"Error while matching the context to an exit code:\n{ExitCode.__format_exc()}")
            ExitCode.__logger.info(f"Exiting with exit code {ExitCode.EXIT_CODE_MATCHING_EXCEPTION}")
            exit(ExitCode.EXIT_CODE_MATCHING_EXCEPTION)
        




flag_documentation = {
    ExitCode.EXIT_CODE_MATCHING_EXCEPTION : "An unseen exception occured while getting the exit code on program exit.",
    ExitCode.UNKNOWN_EXCEPTION : "No valid code could be matched to the exception that caused the program to crash. This should be investigated.",
    ExitCode.KEYBOARD_INTERRUPT : "The program was stopped because of a SIGINT signal (KeyboardInterrupt exception).",
    ExitCode.BAGUETTE_FORMAT_ERROR : "The program crashed because of a corrupted BAGUETTE file.",
    ExitCode.ONTOLOGICAL_WARNING : "The program was aborded because a pattern which does not satisfy BAGUETTE's ontology was used.",
    ExitCode.PARSING_ERROR : "An invalid argument was given as input to the program.",
    ExitCode.PREPARING_EXCEPTION : "Some error occured while preparing an execution report into a BAGUETTE file.",
    ExitCode.BAKING_TIMEOUT : "The baking of a BAGUETTE file reached the timeout set for its compilation.",
    ExitCode.BAKING_UNKNOWN_EXCEPTION : "The baking of a BAGUETTE file resulted in an unknown exception. This should be investigated.",
    ExitCode.BAKING_MISSING_DATA : "The baking of the BAGUETTE file cannot be done as some required behavioral information is missing.",
    ExitCode.TOASTING_UNKNOWN_EXCEPTION : "The toasting of the BAGUETTE file resulted in an unknown exception. This should be investigated.",
    ExitCode.TOASTING_TIMEOUT : "The toasting of a BAGUETTE file reached the timeout set for its extraction.",
    ExitCode.OPENING_GEPHI_RUNTIME_ERROR : "The Gephi process encountered an error while visualizing the BAGUETTE Graph. This should be investigated.",
    ExitCode.OPENING_GEPHI_STARTING_ERROR : "The Gephi process could not be started. This should be investigated.",
}





class ExitCodeParser(ArgumentParser):

    def error(self, message: str) -> NoReturn:
        print(f"error: {message}")
        exit(ExitCode.PARSING_ERROR)





def keyboard_interrupt_exit(exc : BaseException | None, **kwargs):
    if isinstance(exc, KeyboardInterrupt):
        from .logger import logger
        logger.info("Caught a KeyboardInterrupt.")
        print("Exiting.")
        return True
    return False

ExitCode.KEYBOARD_INTERRUPT.register_error_code_checker(keyboard_interrupt_exit)
del keyboard_interrupt_exit
    




del ArgumentParser, IntFlag, auto, nonmember, Any, NoReturn, Protocol, format_exc, format_exception, exception

def main():

    def flag_converter(s : str):
        try:
            f = int(s)
            return ExitCode(f)
        except:
            if s in ExitCode.__members__:
                return ExitCode.__members__[s]
            parser.error(f"Could not recognize flag: '{s}'")

    parser = ExitCodeParser(
        "baguette.exit_codes",
        description="Allows you to interact with and learn about the different BAGUETTE exit codes. Choose one of the following commands to use this tool. Defaults to 'translate'.",
        epilog="Note that these error codes can be mixed (ORed) by some programs if multiple errors occur.",
        add_help=False)
    
    parser.add_argument("--help", "-h", action="store_true", help="show this help message and exit")

    args, remaining = parser.parse_known_args()
    
    subparsers = parser.add_subparsers(dest="command", required=False)

    ls = subparsers.add_parser("list", aliases=["ls"], description="Lists all the exit codes with their documentation and exits.")
    translate = subparsers.add_parser("translate", description="Accepts any exit code as names or integers, combines them, prints the names and the value, and exits with this value as exit code.")

    default = False
    if not remaining or remaining[0] not in ("ls", "list", "translate"):
        remaining.insert(0, "translate")
        default = True

    args, remaining = parser.parse_known_args(remaining, args)

    translate.add_argument("flags", nargs="+", type=flag_converter, help="The flag(s) to convert. Either integer or flag names. If multiple flags are given, they are ORed and decomposed into primary flags.")
    translate.add_argument("--no-exit-code", action="store_true", help="If this option is given, the return code of this program is zero instead of the translated flags.")

    if args.help:
        if default:
            parser.print_help()
        elif args.command == "translate":
            translate.print_help()
        elif args.command in ("ls", "list"):
            ls.print_help()
        exit()

    if args.command == "translate":
        args = translate.parse_args(remaining, args)
    elif args.command in ("ls", "list"):
        args = ls.parse_args(remaining, args)
    else:
        raise RuntimeError("No command detected")

    if args.command in ("list", "ls"):
        print("\nExisting exit codes are:\n")
        for code, doc in flag_documentation.items():
            print(f"({code.value}) {code.name} : {doc}")
        print()
        exit()

    flags : list[ExitCode] = args.flags

    f = ExitCode(0)
    for fi in flags:
        f |= fi
    
    if f:
        print(f"{f.value} : {" | ".join(fi.name if fi.name else "<UNKNOWN FLAG>" for fi in f)}")
    else:
        print(0)
    
    if not args.no_exit_code:
        exit(f)

if __name__ == "__main__":
    main()

del flag_documentation, logger