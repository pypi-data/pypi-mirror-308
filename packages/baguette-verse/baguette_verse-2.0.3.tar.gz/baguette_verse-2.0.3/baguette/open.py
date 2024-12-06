"""
This module contains the code that the system will call to interact with BAGUETTE files.
It is the common entry point.
"""





def main():
    """
    This function is called when opening a BAGUETTE file from a terminal. Flags given in the command line redirect to the adequate entry point.
    """

    import logging
    from subprocess import run
    from pathlib import Path
    from tempfile import TemporaryDirectory
    from traceback import format_exc
    from typing import Literal
    from sys import argv
    from .filesystem.baguette_file import BaguetteFile
    from .bakery.source.types.utils import behavioral_packages
    from .bakery.source import graph
    from .croutons.source import metagraph
    from .exit_codes import ExitCodeParser, ExitCode
    from .logger import logger, set_level

    parser = ExitCodeParser("baguette.open", description="Script to load a BAGUETTE Graph in the current Python interpreter or run another BAGUETTE command.", exit_on_error=False)

    parser.add_argument("baguette", type=Path, help="The path to the BAGUETTE file (.bag) to open.")
    subparsers = parser.add_subparsers(dest="command", required=False)
    visualize = subparsers.add_parser("gephi", aliases=["visual", "visualize"], help="Opens Gephi to visualize the BAGUETTE Graph.")
    bake = subparsers.add_parser("bake", aliases=["compile"], help="Performs the compilation (baking) of the report stored in the BAGUETTE file. Use 'bake -h' for more info.")
    toast = subparsers.add_parser("toast", aliases=["extract"], help="Performs the extraction (toasting) of the BAGUETTE Graph stored in the file. Use 'toast -h' for more info.")

    parser.add_argument("--readonly", action="store_true", help="If this flag is set, runs the interactive prompt with the BAGUETTE file in readonly mode.")
    parser.add_argument("--verbosity", "-v", action="count", default=0, help="Increases the verbosity of the output.")

    if len(argv) > 2 and argv[2] == "":
        argv.pop(2)

    args = parser.parse_args()

    levels = {
        0 : logging.ERROR,
        1 : logging.WARNING,
        2 : logging.INFO,
        3 : logging.DEBUG
    }
    verbosity : Literal[0, 1, 2, 3] = min(3, args.verbosity)
    set_level(levels[verbosity])

    logger.info("Arguments parsed.")

    command : Literal["gephi", "visual", "visualize", "bake", "compile", "toast", "extract"] | None = args.command

    def wait_for_closing():
        input("Press Enter to exit")
        exit(ExitCode.PARSING_ERROR)

    baguette_path : Path = args.baguette

    if not baguette_path.exists():
        parser.error(f"BAGUETTE file does not exist: '{baguette_path}'")
        wait_for_closing()
    if not baguette_path.is_file():
        parser.error(f"BAGUETTE file exists and is not a file: '{baguette_path}'")
        wait_for_closing()

    logger.debug("Opening BAGUETTE file.")

    baguette = BaguetteFile(baguette_path, mode = "r" if args.readonly else None)

    if command in ("gephi", "visual", "visualize"):

        logger.info("Mode is 'gephi'. Opening and preparing Graph.")

        with TemporaryDirectory() as tmp_dir:
            try:
                cmd = None
                gephi_file = Path(tmp_dir) / f"{baguette_path.stem}.gexf"
                logger.debug("Filtering and exporting Graph as Gephi format in tmp directory.")
                baguette.filtered_baguette.export(f"{gephi_file}")
                from .setup.preferences import infer_gephi_path
                cmd = [f"{infer_gephi_path()}", f"{gephi_file}"]
                logger.debug("Starting Gephi process.")
                run(cmd)
                code = ExitCode(0)
            except:
                if cmd is not None:
                    logger.error(f"An exception occured when starting the Gephi process. The command line was : {cmd}\n{format_exc()}")
                    code = ExitCode.OPENING_GEPHI_STARTING_ERROR
                else:
                    logger.error(f"An exception occured when before starting the Gephi process:\n{format_exc()}")
                    code = ExitCode.OPENING_GEPHI_RUNTIME_ERROR
                input("\nPress Enter to exit")
            finally:
                ExitCode.exit(code)

    elif command in ("bake", "compile"):

        logger.info("Mode is 'bake'. Opening report and building Graph.")
        
        if not baguette.has_report():
            parser.error("BAGUETTE file has no affected report")
            wait_for_closing()
        
        if not baguette.has_baguette():
            from .bakery.compiler import compile
            from .bakery.source.parsers.utils import MissingBehavioralInfoError, MissingSamplePathError
            try:
                logger.debug("Starting compilation process.")
                compile(baguette)
                logger.debug("Compilation process complete.")
                ExitCode.exit()
            except SystemExit:
                raise
            except KeyboardInterrupt:
                ExitCode.exit()
            except:
                logger.error(f"Got a baking exception:\n{format_exc()}")
                input("\nPress Enter to exit")
                ExitCode.exit(ExitCode.BAKING_MISSING_DATA if baguette.metadata.compilation_parameters.exception is not None and issubclass(baguette.metadata.compilation_parameters.exception.exc_type, (MissingSamplePathError, MissingBehavioralInfoError)) else ExitCode.BAKING_UNKNOWN_EXCEPTION)

    elif command in ("toast", "extract"):

        logger.info("Mode is 'toast'. Opening Graph and searching patterns.")
        
        if not baguette.has_baguette():
            parser.error("BAGUETTE file has not yet been baked")
            wait_for_closing()

        if not baguette.has_matches():
            from .croutons.extractor import extract
            try:
                logger.debug("Starting extraction process.")
                extract(baguette)
                logger.debug("Extraction process complete.")
                ExitCode.exit()
            except SystemExit:
                raise
            except KeyboardInterrupt:
                ExitCode.exit()
            except:
                logger.error(f"Got a toasting exception:\n{format_exc()}")
                input("\nPress Enter to exit")
                ExitCode.exit(ExitCode.TOASTING_UNKNOWN_EXCEPTION)

    else:

        logger.info("Mode is 'interactive'. Preparing interactive interpreter.")

        from Viper.interactive import InteractiveInterpreter
        try:
            logger.debug("Preparing BAGUETTE interactive environment.")
            env = {
                "bag" : baguette,
            } | behavioral_packages() | {name : getattr(graph, name) for name in graph.__all__} | {name : getattr(metagraph, name) for name in metagraph.__all__}
            logger.debug("Starting interactive prompt.")
            InteractiveInterpreter(env).interact(f"BAGUETTE Interactive Prompt. Variable 'bag' holds the opened BAGUETTE file{" (in readonly mode)" if args.readonly else ""}.\nMost BAGUETTE packages are also loaded. Use dir() and help() to find out more.")
            ExitCode.exit()
        except SystemExit:
            raise
        except:
            logger.error(f"An exception occured when starting the interactive interpreter:\n{format_exc()}")
            input("\nPress Enter to exit")
            ExitCode.exit()





if __name__ == "__main__":
    main()