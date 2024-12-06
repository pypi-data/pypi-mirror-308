"""
This is a *magic* script to toast BAGUETTEs. Use -h/--help for usage.
"""




def main():
    """
    Command line function to toast baguettes. Use -h/--help for more info.
    """

    import logging

    from .logger import logger, set_level
    set_level(logging.ERROR)

    from .progress import ProgressBar
    from math import isnan
    from re import compile as recompile
    from pathlib import Path
    from os import environ, cpu_count
    from typing import Literal, Iterable

    from Viper.collections.isomorph import IsoDict, IsoSet
    from Viper.pickle_utils import RestrictiveUnpickler, ForbiddenPickleError

    from .filesystem.fluid_path import FluidPath
    from .croutons.extractor import extract, ToastingTimeout
    from .croutons.source.metagraph import MetaGraph, FrozenMetaGraph, MetaEdge, MetaVertex
    from .croutons.source.evaluator import Evaluator
    from .bakery.source.graph import Vertex, Edge, Graph
    from .bakery.source.colors import Color
    from .filesystem import BaguetteFile
    from .exit_codes import ExitCode, ExitCodeParser

    parser = ExitCodeParser(
        "toast",
        description = 'Searches for the selected patterns in BAGUETTE files.',
        add_help = False,
        conflict_handler = 'resolve',
        epilog="""
        Note that this help changes depending if the environment variables 'BAGUETTE_BAGS' and 'BAGUETTE_PATTERNS' are set.
        Both holds paths to directories with respectively all the BAGUETTE files and all the pattern files.
        """
        )

    def pool_size(arg : str) -> int:
        """
        Transforms a numeric argument in a number of process to use as a process pool.
        It can be absolute, negative (relative to the number of CPUs) or proportion greater than 0.
        """
        N = cpu_count()
        if not N:
            N = 1
        try:
            v = int(arg)
            if v < 0:
                v = N - v
            if v <= 0:
                parser.error("got a (too) negative value for process pool size : '{}'".format(arg))
        except:
            try:
                v = float(arg)
                if v <= 0:
                    parser.error("got a negative relative process pool size : '{}'".format(arg))
                v = round(v * N)
            except:
                parser.error("not a process pool size : '{}'".format(arg))
        return v

    def time(arg : str) -> float:
        try:
            v = float(arg)
            if v <= 0 or isnan(v):
                parser.error("got a negative, null or nan maxtime")
            return v
        except:
            parser.error("expected positive float for maxtime, got : '{}'".format(arg))

    def paint_color(c : str) -> Color:
        if c in dir(Color):
            color = getattr(Color, c.lower())
            if not isinstance(color, Color):
                parser.error(f"not a valid color name : '{c}'")
            return color
        else:
            # We can match colors in ALL LANGUAGES!!!!
            color_re = r"([\d\.eE-]+|\d+|0[xX][\daAbBcCdDeEfF]+)"
            sep_re = r"(?:[ ,;:\|\&]+)"
            inner_expr = r"(?:" + color_re + sep_re + color_re + sep_re + color_re + r")"
            fmatch = recompile(inner_expr).fullmatch(c) or recompile(r"\(" + inner_expr + r"\)").fullmatch(c) or recompile(r"\[" + inner_expr + r"\]").fullmatch(c) or recompile(r"\{" + inner_expr + r"\}").fullmatch(c)
            if not fmatch:
                parser.error(f"could not understand color format : '{c}'")
            r, g, b = fmatch.groups()

            def is_float(s : str) -> bool:
                try:
                    f = float(s)
                    if not 0 <= f <= 1:
                        return False
                    return True
                except:
                    return False
            
            def is_int(s : str) -> bool:
                try:
                    i = int(s)
                    if not 0 <= i <= 255:
                        return False
                    return True
                except:
                    return False
            
            def is_hex(s : str) -> bool:
                try:
                    i = int(s, base=16)
                    if not 0 <= i <= 255:
                        return False
                    return True
                except:
                    return False
                
            if all(is_float(x) for x in (r, g, b)):
                r, g, b = float(r), float(g), float(b)
            elif all(is_int(x) for x in (r, g, b)):
                r, g, b = int(r), int(g), int(b)
            elif all(is_hex(x) for x in (r, g, b)):
                r, g, b = int(r, 16), int(g, 16), int(b, 16)
            else:
                parser.error(f"could not understand color format : '{c}'")

            return Color(r, g, b)
    
    def writable_fluid_path(arg : str) -> FluidPath:
        return FluidPath(arg, allow_zip=False)

    args, _ = parser.parse_known_args()
    parser.add_argument("--help", "-h", action="help", help="Shows this help and exits.")
    
    if "BAGUETTE_BAGS" in environ:
        parser.add_argument("--baguettes", "-b", type=writable_fluid_path, default=None, action="extend", help="BAGUETTE files in which to search for the patterns and save them. Can also be a wildcard expression. Defaults to environment variable 'BAGUETTE_BAGS'.")
    else:
        parser.add_argument("baguettes", type=writable_fluid_path, nargs="+", help="BAGUETTE files in which to search for the patterns and save them. Can also be a wildcard expression. Would default to environment variable 'BAGUETTE_BAGS' if it was set.")

    if "BAGUETTE_PATTERNS" in environ:
        parser.add_argument("--patterns", "-p", type=FluidPath, action="extend", nargs="*", help="The path(s) to the input pattern files to search for in BAGUETTE Graphs. If not given, the BAGUETTE files must already have some patterns affected. These files must contain pickles of iterables of MetaGraphs. Accepts wildcards and can look into zip files. Defaults to environment variable 'BAGUETTE_PATTERNS'.")
    else:
        parser.add_argument("--patterns", "-p", type=FluidPath, action="extend", nargs="*", help="The path(s) to the input pattern files to search for in BAGUETTE Graphs. If not given, the BAGUETTE files must already have some patterns affected. These files must contain pickles of iterables of MetaGraphs. Accepts wildcards and can look into zip files. Would defaults to environment variable 'BAGUETTE_PATTERNS' if it was set.")

    parser.add_argument("--pool", "--ncpus", type=pool_size, default=pool_size("0.5"), help="The size of the process pool to use to toast in parallel.")
    color_override = parser.add_mutually_exclusive_group()
    color_override.add_argument("--paint-color", "-c", type=paint_color, default=None, help="If given, the colors of each pattern will be replaced by this color.")
    color_override.add_argument("--no-paint", action="store_true", help="If this flag is set, the matches of the patterns will not be painted in the BAGUETTE Graphs.")
    parser.add_argument("--timeout", "--maxtime", "-m", type=time, default=time("inf"), help="The maximum amount of time spent searching for patterns across a single baguette. No maxtime by default.")
    parser.add_argument("--verbosity", "-v", action="count", default=0, help="Increases the verbosity of the output.")
    parser.add_argument("--perf", action="store_true", default=False, help="If this is enabled, a performance report will be printed at the end of the toasting process.")

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

    # Parsing jobs

    logger.debug("Analyzing input BAGUETTE paths.")

    abstract_baguettes_files : list[FluidPath] | None = args.baguettes
    if abstract_baguettes_files is None:
        abstract_baguettes_files = [FluidPath(str(Path(environ["BAGUETTE_BAGS"], "*")))]
    baguette_file_paths : list[Path] = []
    for p in abstract_baguettes_files:
        baguette_file_paths.extend(Path(str(pi)) for pi in p.expand())

    if not baguette_file_paths:
        parser.error("Found no existing input BAGUETTE file")

    logger.debug("Analyzing input pattern paths.")

    abstract_pattern_files : list[FluidPath] | None = args.patterns
    if abstract_pattern_files is None:
        if"BAGUETTE_PATTERNS" in environ:
            abstract_pattern_files = [FluidPath(str(Path(environ["BAGUETTE_PATTERNS"], "*")))]
        else:
            abstract_pattern_files = []
    pattern_file_paths : list[Path] = []
    for p in abstract_pattern_files:
        pattern_file_paths.extend(Path(str(pi)) for pi in p.expand())

    if pattern_file_paths:

        logger.info("Gathering patterns and paint colors.")
        patterns : set[FrozenMetaGraph] | None = set()
        for p in pattern_file_paths:
            unpickler = RestrictiveUnpickler()
            for cls in (Graph, MetaVertex, MetaEdge, Vertex, Edge, Color, Evaluator, IsoDict, IsoSet):
                unpickler.allow_class_hierarchy(cls)
            try:
                with p.open("rb") as f:
                    while data := f.read(2 ** 20):
                        unpickler.write(data)
                    obj = unpickler.load()
            except ForbiddenPickleError:
                parser.error(f"Pattern file '{p}' does not contain an iterable of MetaGraphs.")
            if not isinstance(obj, Iterable):
                parser.error(f"Pattern file '{p}' does not contain the pickle of an iterable.")
            for e in obj:
                if isinstance(e, MetaGraph):
                    if not isinstance(e, FrozenMetaGraph):
                        e = FrozenMetaGraph(e)
                    patterns.add(e)
                else:
                    parser.error(f"Pattern file '{p}' does not contain an iterable of MetaGraphs. Found '{e}' in iterable.")
        
    else:
        
        logger.info("No input pattern file. Using patterns affected to each BAGUETTE file.")
        patterns = None

    work = baguette_file_paths

    # Extract now...

    from multiprocessing import Process
    from threading import Lock, Thread

    # All of this is because multiprocessing was coded with feet... Pool's async methods may freeze (deadlock maybe) on some platforms.

    lock = Lock()
    timeout : float = args.timeout
    perf : bool = args.perf
    no_paint : bool = args.no_paint
    color : Color | None  = args.paint_color
    failed, timed_out, total = 0, 0, len(work)

    def execute_single_job() -> bool:
        nonlocal failed, timed_out
        with lock:
            if not work:
                return False
            baguette_path = work.pop()
        logger.debug(f"Affecting extraction parameters to BAGUETTE at '{baguette_path}'")
        baguette = BaguetteFile(baguette_path)
        ep = baguette.metadata.extraction_parameters
        ep.verbosity = verbosity
        ep.timeout = timeout
        ep.perf = perf
        ep.paint_color = False if no_paint else color
        if patterns is not None:
            baguette.patterns = patterns
        baguette.close()
        proc = Process(target=extract, args=(baguette_path, ), daemon=True)
        proc.start()
        proc.join()
        bar.current += 1
        baguette = BaguetteFile(baguette_path, mode = "r")
        remote_exception_traceback = baguette.metadata.extraction_parameters.exception
        if remote_exception_traceback is not None and issubclass(remote_exception_traceback.exc_type, KeyboardInterrupt):
            return False
        elif remote_exception_traceback is not None and not issubclass(remote_exception_traceback.exc_type, ToastingTimeout):
            with lock:
                failed += 1
            logger.error(f"Got a '{remote_exception_traceback.exc_type.__name__}' error during the toasting of '{baguette.path}'.")
        elif remote_exception_traceback is not None and issubclass(remote_exception_traceback.exc_type, ToastingTimeout):
            with lock:
                timed_out += 1
        return True

    def executor():
        while execute_single_job():
            pass
    
    threads : list[Thread] = []
    try:
        logger.debug("Preparing multiprocessing pool.")
        n_workers = min(args.pool, len(work))
        with ProgressBar(f"Toasting BAGUETTE files") as bar:
            bar.total = len(work)
            for _ in range(n_workers):
                t = Thread(target = executor, daemon = True)
                t.start()
                threads.append(t)

            logger.info("All workers started. Awaiting results.")
            for t in threads:
                t.join()
        
        success = total - failed - timed_out
        if failed and success and timed_out:
            print("{} failed toasts, {} took too long and {} well-toasted.".format(failed, timed_out, success))
        elif failed and success:
            print("{} failed toasts, {} toasted correctly.".format(failed, success))
        elif timed_out and success:
            print("{} baguettes took too long to toast, {} toasted correctly.".format(timed_out, success))
        elif failed and timed_out:
            print("{} toasts are failed and the {} others took too long to toast...".format(failed, timed_out))
        elif failed:
            print("All {} baguettes did not toast correctly...".format(failed))
        elif timed_out:
            print("All {} baguettes took too long to toast...".format(timed_out))
        elif success:
            print("All {} are well-toasted!".format(success))
        ExitCode.exit(ExitCode(0) if not failed else ExitCode.TOASTING_UNKNOWN_EXCEPTION, ExitCode(0) if not timed_out else ExitCode.TOASTING_TIMEOUT)
    except SystemExit:
        raise
    except:
        ExitCode.exit()
            




if __name__ == "__main__":
    main()