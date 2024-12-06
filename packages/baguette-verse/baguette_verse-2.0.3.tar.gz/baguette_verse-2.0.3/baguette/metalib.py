"""
This module can be launched to run an interactive session to work with MetaGraphs.
"""

__all__ = ["main"]





def main():

    import logging

    from .logger import set_level

    set_level(logging.WARNING)

    from Viper.interactive import InteractiveInterpreter
    from pathlib import Path
    from typing import Literal, Iterable
    from os import environ
    from .filesystem.fluid_path import FluidPath
    from .logger import logger
    from .exit_codes import ExitCode, ExitCodeParser

    parser = ExitCodeParser("metalib", description="""
    Starts the metalib or performs other actions.
    The metalib is a system to manage MetaGraph patterns.
    Without arguments, opens a interactive prompt to create, load and save MetaGraphs.
    """)

    def writable_fluid_path(arg : str) -> FluidPath:
        return FluidPath(arg, allow_zip=False)

    subparsers = parser.add_subparsers(dest="command", required=False)
    list_parser = subparsers.add_parser("list", aliases=["ls"], help="Lists all existing patterns in the metalib by names.")
    list_parser.add_argument("--separator", type=str, default="\n", help="The separator between the names.")
    list_parser.add_argument("--quotes", type=str, default="'", help="The quotes to use around the names.")
    list_parser.add_argument("--pattern", type=str, default="*", help="A wildcard pattern to apply for filtering the names.")
    export_parser = subparsers.add_parser("export", aliases=["save"], help="Exports MetaGraph patterns to a file.")
    export_parser.add_argument("names", nargs="*", type=str, help="The pattern names in the metalib to export. Supports wildcards. Defaults to all patterns.")
    export_parser.add_argument("--output", "-o", type=Path, default=None, help="The output file. This file will contain the pickle of the list of all exported MetaGraphs. Defaults to stdout")
    import_parser = subparsers.add_parser("import", aliases=["load"], help="Imports MetaGraphs with names from a file.")
    import_parser.add_argument("input", type=Path, nargs="?", help="The input file. Must contain the pickle of an iterable of couples of (MetaGraph, str) representing each pattern with its new name in the metalib. If it is a dictionary, dict.items() is used. Defaults to stdin.")
    decorate_parser = subparsers.add_parser("decorate", aliases=["flavor"], help="Decorates BAGUETTE files with patterns of the metalib for toasting.")
    if "BAGUETTE_BAGS" in environ:
        decorate_parser.add_argument("--baguettes", "-b", type=writable_fluid_path, default=None, action="extend", help="The BAGUETTE files to decorate. Can also be a wildcard expression. Defaults to environment variable 'BAGUETTE_BAGS'.")
    else:
        decorate_parser.add_argument("baguettes", type=writable_fluid_path, nargs="+", help="The BAGUETTE files to decorate. Can also be a wildcard expression. Would default to environment variable 'BAGUETTE_BAGS' if it was set.")
    decorate_parser.add_argument("--pattern", type=str, default="*", help="A wildcard pattern to apply for filtering the MetaGraph pattern names in the metalib.")
    parser.add_argument("--verbosity", "-v", action="count", default=0, help="Increases the verbosity of the output.")

    args = parser.parse_args()

    # Setting logging level

    levels = {
        0 : logging.ERROR,
        1 : logging.WARNING,
        2 : logging.INFO,
        3 : logging.DEBUG
    }
    verbosity : Literal[0, 1, 2, 3] = min(3, args.verbosity)
    set_level(levels[verbosity])

    logger.info("Arguments parsed. Discovering jobs.")

    command : Literal["list", "ls", "export", "save", "import", "load", "decorate", "flavor"] | None = args.command

    logger.info(f"Received command '{command}'." if command is not None else "Received no command.")

    if command in ("list", "ls"):

        from .croutons.metalib.utils import entries
        from fnmatch import fnmatch, fnmatchcase
        from sys import platform
        separator : str = args.separator
        quotes : str = args.quotes
        pattern : str = args.pattern
        if platform == "win32":
            matcher = fnmatch
        else:
            matcher = fnmatchcase
        names = [name for name in entries() if matcher(name, pattern)]

        print(separator.join(f"{quotes}{name}{quotes}" for name in names))

    elif command in ("export", "save"):

        from .croutons.metalib.utils import entries, load
        from fnmatch import fnmatch, fnmatchcase
        from pickle import dump
        from sys import platform, stdout
        raw_names : list[str] = args.names
        output : Path | None = args.output


        if output is not None and output.exists() and not output.is_file():
            parser.error(f"output path exists and is not a file: '{output}'")
        if not raw_names:
            raw_names = ["*"]
        
        if platform == "win32":
            matcher = fnmatch
        else:
            matcher = fnmatchcase
        names = [name for name in entries() if any(matcher(name, raw_name) for raw_name in raw_names)]
        
        if output is not None:
            with output.open("wb") as f:
                dump({load(name) : name for name in names}, f)
        else:
            dump({load(name) : name for name in names}, stdout.buffer)

    elif command in ("import", "load"):

        from sys import stdin
        from Viper.collections.isomorph import IsoDict, IsoSet
        from Viper.pickle_utils import RestrictiveUnpickler, ForbiddenPickleError
        from .bakery.source.graph import Vertex, Edge, Graph
        from .bakery.source.colors import Color
        from .croutons.source.evaluator import Evaluator
        from .croutons.source.metagraph import MetaGraph, MetaEdge, MetaVertex
        from .croutons.metalib.utils import save
        from .progress import ProgressBar
        
        input : Path | None = args.input
        if input is not None:
            if not input.exists():
                parser.error(f"no such input file: '{input}'")
            if not input.is_file():
                parser.error(f"input path exists but is not a file: '{input}'")

        unpickler = RestrictiveUnpickler()
        for cls in (Graph, MetaVertex, MetaEdge, Vertex, Edge, Color, Evaluator, IsoSet, IsoDict):
            unpickler.allow_class_hierarchy(cls)

        if input is not None:
            with input.open("rb") as f:
                try:
                    while data := f.read(2 ** 20):
                        unpickler.write(data)
                    obj = unpickler.load()
                except ForbiddenPickleError:
                    parser.error("input file does not contain an iterable of couples of MetaGraphs anf str")
        else:
            try:
                while True:
                    with unpickler.writable as n:
                        if not n:
                            break
                        data = stdin.buffer.read(n)
                    unpickler.write(data)
                obj = unpickler.load()
            except ForbiddenPickleError:
                parser.error("input does not contain an iterable of couples of MetaGraphs anf str")
        
        if not isinstance(obj, Iterable):
            parser.error(f"input file does not contain an iterable but a '{type(obj).__name__}'")
        if isinstance(obj, dict):
            obj = obj.items()
        patterns : dict[MetaGraph, str] = {}
        existing_names : set[str] = set()
        obj = list(obj)

        with ProgressBar("Analyzing patterns from input file") as bar:
            bar.progress = len(obj)
            for k in obj:
                if not isinstance(k, tuple):
                    parser.error(f"input file does not contain an iterable of tuples: found a '{type(k).__name__}'")
                if len(k) != 2:
                    parser.error(f"input file does not contain an iterable of couples: found a length {len(k)} tuple")
                a, b = k
                if isinstance(a, MetaGraph) and isinstance(b, str):
                    mg, name = a, b
                elif isinstance(a, str) and isinstance(b, MetaGraph):
                    mg, name = b, a
                else:
                    parser.error(f"input file does not contain an iterable of couples of MetaGraphs and str: found a ('{type(a).__name__}', '{type(b).__name__}') couple")
                if name in existing_names and patterns.get(mg) != name:
                    parser.error(f"input file contains a name collision: '{name}'")
                if mg in patterns and patterns[mg] != name:
                    parser.error(f"input file contains a pattern collision: '{name}' and '{patterns[mg]}'")
                patterns[mg] = name
                existing_names.add(name)
                bar.current += 1
        
        with ProgressBar("Saving patterns to metalib") as bar:
            bar.total = len(patterns)
            for mg, name in patterns.items():
                save(mg, name)
                bar.current += 1

    elif command in ("decorate", "flavor"):

        from alive_progress import alive_bar
        from sys import platform
        from fnmatch import fnmatch, fnmatchcase
        from .croutons.metalib.utils import entries, load
        from .filesystem import BaguetteFile

        abstract_baguettes_files : list[FluidPath] | None = args.baguettes
        if abstract_baguettes_files is None:
            abstract_baguettes_files = [FluidPath(str(Path(environ["BAGUETTE_BAGS"], "*")))]
        baguette_file_paths : list[Path] = []
        for p in abstract_baguettes_files:
            baguette_file_paths.extend(Path(str(pi)) for pi in p.expand())

        if not baguette_file_paths:
            parser.error("Found no existing input BAGUETTE file")

        pattern : str = args.pattern
        if platform == "win32":
            matcher = fnmatch
        else:
            matcher = fnmatchcase
        pattern_list = [load(name) for name in entries() if matcher(name, pattern)]

        with alive_bar(len(baguette_file_paths), title="Decorating BAGUETTE files with metalib patterns") as bar:
            for p in baguette_file_paths:
                f = BaguetteFile(p)
                f.patterns = pattern_list
                bar()

    else:

        env = {}

        from .croutons.metalib import utils

        utils.import_env(env)
        for name in utils.__all__:
            env[name] = getattr(utils, name)

        env.pop("import_env")

        InteractiveInterpreter(env).interact("MetaLib interactive console.\nUse save(MG, name) and load(name) to save and load MetaGraphs.\nUse entries() to get a list of all MetaGraphs available in the library.\nUse remove(name) to delete a MetaGraph from the library.\nAll useful types are loaded, including Graph and MetaGraph related types.")





if __name__ == "__main__":
    main()