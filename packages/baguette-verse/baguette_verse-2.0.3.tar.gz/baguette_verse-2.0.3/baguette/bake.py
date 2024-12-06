"""
This is a *magic* script to bake BAGUETTEs. Use -h/--help for usage.
"""





def main():
    """
    Command line function to bake execution report(s). Use -h/--help for more info.
    """

    import logging

    from .logger import logger, set_level
    set_level(logging.ERROR)

    from math import isnan
    from re import compile as recompile
    from pathlib import Path
    from os import environ, cpu_count, remove
    from typing import Literal

    from .filesystem.fluid_path import FluidPath
    from .bakery.compiler import compile, BakingTimeout
    from .bakery.source import filters
    from .bakery.source.colors import Color
    from .bakery.source.parsers import parsers, AbstractParser
    from .bakery.source.parsers.utils import MissingBehavioralInfoError, MissingSamplePathError
    from .filesystem import BaguetteFile
    from .exit_codes import ExitCode, ExitCodeParser
    from .progress import ProgressBar

    parser = ExitCodeParser(
        "bake",
        description = 'Bakes execution reports into BAGUETTE Graphs.',
        add_help = False,
        conflict_handler = 'resolve',
        epilog="""
        Note that this help changes depending if the flag '--raw' is given and if the environment variables 'BAGUETTE_REPORTS' and 'BAGUETTE_BAGS' are set.
        Both holds paths to directories with respectively all the execution reports and the BAGUETTE files.
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
    
    def output_folder_matcher(arg : str) -> Path:
        try:
            try:
                path = Path(arg)
            except:
                parser.error(f"malformed output directory path: '{arg}'.")
            if path.exists() and not path.is_dir():
                parser.error(f"output directory exists and is not a directory: '{arg}'.")
            if not path.exists():
                path.mkdir(parents=True)
            return path
        except PermissionError:
            parser.error(f"Cannot access this output folder: '{arg}'. Permission denied.")

    def writable_fluid_path(arg : str) -> FluidPath:
        return FluidPath(arg, allow_zip=False)

    mode_switch_arg = parser.add_argument("--raw", "--prepare", action="store_true")
    args, _ = parser.parse_known_args()
    parser.add_argument("--help", "-h", action="help", help="Shows this help and exits.")

    if args.raw:
        mode_switch_arg.help = "If this flag is removed, switches to prepared input mode, which expects BAGUETTE files that contain a Cuckoo report."
        if "BAGUETTE_REPORTS" in environ:
            parser.add_argument("--reports", "-r", type=FluidPath, action="extend", help="The path(s) to the input execution report(s) to bake into a BAGUETTE file. Accepts wildcards and can look into zip files. Defaults to environment variable 'BAGUETTE_REPORTS'. Parameter '--raw' changes its behavior.")
        else:
            parser.add_argument("reports", type=FluidPath, nargs="+", help="The path(s) to the input execution report(s) to bake into a BAGUETTE file. Accepts wildcards and can look into zip files. Would default to environment variable 'BAGUETTE_REPORTS' if it was set. Parameter '--raw' changes its behavior.")
        if "BAGUETTE_BAGS" in environ:
            parser.add_argument("--output", "-o", type=output_folder_matcher, default=None, help="The output folder where all the BAGUETTE files will be put into. Defaults to environment variable 'BAGUETTE_BAGS'. Parameter '--raw' changes its behavior.")
        else:
            parser.add_argument("output", type=output_folder_matcher, help="The output folder where all the BAGUETTE files will be put into. Would default to environment variable 'BAGUETTE_BAGS' if it was set. Parameter '--raw' changes its behavior.")
    
    else:
        mode_switch_arg.help = "If this flag is given, switches to raw input mode, which expects execution reports instead of BAGUETTE files."
        if "BAGUETTE_BAGS" in environ:
            parser.add_argument("--baguettes", "-b", type=writable_fluid_path, default=None, action="extend", help="BAGUETTE files containing the execution reports to bake. Can also be a wildcard expression. Defaults to environment variable 'BAGUETTE_BAGS'. Parameter '--raw' changes its behavior.")
        else:
            parser.add_argument("baguettes", type=writable_fluid_path, nargs="+", help="BAGUETTE files containing the execution reports to bake. Can also be a wildcard expression. Would default to environment variable 'BAGUETTE_BAGS' if it was set. Parameter '--raw' changes its behavior.")

    parser.add_argument("--pool", "--ncpus", type=pool_size, default=pool_size("0.5"), help="The size of the process pool to use to bake in parallel.")
    parser.add_argument("--timeout", "--maxtime", "-m", type=time, default=time("inf"), help="The maximum amount of time spent baking a single baguette. No maxtime by default.")
    parser.add_argument("--report-type", "--report-format", "-t", type=str, default=AbstractParser.report_name, choices=[p.report_name for p in parsers], help="The type of execution report used as a source. Tries to autodetect for each sample by default.")
    parser.add_argument("--filters", type=str, default=[], choices=[name for name in dir(filters) if isinstance(getattr(filters, name), filters.Filter)], nargs="*", help="A list of filters that can be used when exporting the baguette to the visual file (.gexf).")
    parser.add_argument("--idempotent", "-i", action="store_true", default=False, help="If enabled, the compiler will first search for a compiled BAGUETTE graph in the computed output folder. It will (re)compile it if it does not exist, has no BAGUETTE Graph inside, if it timed out or if had different compilation parameters.")
    parser.add_argument("--background", type=paint_color, default=Color.black, help="If a color is given for background, the color settings which are close to the background color will be changed to be more visible on that background. Must be a valid color name or RGB values.")
    parser.add_argument("--verbosity", "-v", action="count", default=0, help="Increases the verbosity of the output.")
    parser.add_argument("--perf", action="store_true", default=False, help="If this is enabled, a performance report will be printed at the end of the baking process.")
    parser.add_argument("--skip-data-comparison", action="store_true", default=False, help="If enabled, the computation of the Levenshtein similarity between all Data nodes will be skipped.")
    parser.add_argument("--skip-diff-comparison", action="store_true", default=False, help="Same as skip_data_comparison but for Diff nodes.")

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

    if args.raw:        # BAGUETTEs have not been prepared yet.

        logger.debug("Unprepared input mode. Analyzing I/O arguments.")

        abstract_input_paths : list[FluidPath] = args.reports
        if not abstract_input_paths and "BAGUETTE_REPORTS" in environ:
            logger.debug("Setting input path(s) from environment variable.")
            abstract_input_paths.append(FluidPath(str(Path(environ["BAGUETTE_REPORTS"], "*"))))
        input_paths : list[FluidPath] = []
        logger.debug("Expanding input paths.")
        for p in abstract_input_paths:
            input_paths.extend(p.expand())

        logger.debug("Generating output paths.")
        output_directory : Path | None = args.output
        if output_directory is None:
            output_directory = Path(environ["BAGUETTE_BAGS"])
        baguette_file_paths = [output_directory / f"{Path(str(p)).stem}.bag" for p in input_paths]
        
        if not input_paths:
            parser.error("Found no existing input file")

        logger.debug("Generating work stack.")
        from .bakery.compiler import prepare_and_compile
        work = [(prepare_and_compile, input_path, output_path) for input_path, output_path in zip(input_paths, baguette_file_paths)]

    else:               # BAGUETTEs have already been prepared.

        logger.debug("Prepared input mode. Analyzing input arguments.")

        abstract_baguettes_files : list[FluidPath] | None = args.baguettes
        if abstract_baguettes_files is None:
            abstract_baguettes_files = [FluidPath(str(Path(environ["BAGUETTE_BAGS"], "*")))]
        baguette_file_paths : list[Path] = []
        for p in abstract_baguettes_files:
            baguette_file_paths.extend(Path(str(pi)) for pi in p.expand())

        if not baguette_file_paths:
            parser.error("Found no existing input BAGUETTE file")

        logger.debug("Generating work stack.")
        from .bakery.compiler import compile
        work = [(compile, baguette_file_path) for baguette_file_path in baguette_file_paths]

    # Compile now...

    from multiprocessing import Process
    from threading import Lock, Thread

    # All of this is because multiprocessing was coded with feet... Pool's async methods may freeze (deadlock maybe) on some platforms.

    lock = Lock()
    background_color : Color = args.background
    skip_data_comparison : bool = args.skip_data_comparison
    skip_diff_comparison : bool = args.skip_diff_comparison
    timeout : float = args.timeout
    perf : bool = args.perf
    failed, timed_out, total = 0, 0, len(work)
    missing_data = False
    unknown_exception = False

    def execute_single_job() -> bool:
        nonlocal failed, timed_out, missing_data, unknown_exception
        with lock:
            if not work:
                return False
            job = work.pop()
            func, func_args, baguette_path = job[0], job[1:], job[-1]
        logger.debug(f"Affecting compilation parameters to BAGUETTE at '{baguette_path}'")
        baguette = BaguetteFile(baguette_path)
        cp = baguette.metadata.compilation_parameters
        skip = False
        if not args.raw and args.idempotent and baguette.baked and cp.background_color == background_color and cp.skip_data_comparison == skip_data_comparison and cp.skip_diff_comparison == skip_diff_comparison:
            skip = True
            logger.debug(f"Skipping job as BAGUETTE at '{baguette_path}' has already been baked with this compilation parameters.")
        if not skip:
            logger.debug(f"New job started for arguments '{func_args}'.")
            cp.background_color = background_color
            cp.skip_data_comparison = skip_data_comparison
            cp.skip_diff_comparison = skip_diff_comparison
            cp.verbosity = verbosity
            cp.timeout = timeout
            cp.perf = perf
            baguette.visual_filters = args.filters
            baguette.close()
            proc = Process(target=func, args=func_args, daemon=True)
            proc.start()
            proc.join()
            bar.current += 1
        baguette = BaguetteFile(baguette_path, mode = "r")
        try:
            remote_exception_traceback = baguette.metadata.compilation_parameters.exception
            if remote_exception_traceback is not None and issubclass(remote_exception_traceback.exc_type, KeyboardInterrupt):
                return False
            elif remote_exception_traceback is not None and not issubclass(remote_exception_traceback.exc_type, BakingTimeout):
                with lock:
                    failed += 1
                    if issubclass(remote_exception_traceback.exc_type, (MissingSamplePathError, MissingBehavioralInfoError)):
                        missing_data = True
                    else:
                        unknown_exception = True
                logger.error(f"Got a '{remote_exception_traceback.exc_type.__name__}' error during the baking of '{baguette.path}'.")
            elif remote_exception_traceback is not None and issubclass(remote_exception_traceback.exc_type, BakingTimeout):
                with lock:
                    timed_out += 1
            return True
        finally:
            if baguette.metadata.compilation_parameters.suppressed and baguette.baked and not baguette.has_baguette():
                baguette.close()
                remove(baguette.path)

    def executor():
        while execute_single_job():
            pass
    
    threads : list[Thread] = []
    try:
        logger.debug("Preparing multiprocessing pool.")
        n_workers = min(args.pool, len(work))
        with ProgressBar("Baking BAGUETTE files") as bar:
            bar.total = len(work)
            for _ in range(n_workers):
                t = Thread(target = executor, daemon = True)
                t.start()
                threads.append(t)

            logger.info("All workers started. Awaiting results.")
            for t in threads:
                t.join()
        
        logger.info("All jobs finished. Printing results.")
        success = total - failed - timed_out
        if failed and success and timed_out:
            print("{} failed baguettes, {} took too long and {} well-baked.".format(failed, timed_out, success))
        elif failed and success:
            print("{} failed baguettes, {} baked correctly.".format(failed, success))
        elif timed_out and success:
            print("{} baguettes took too long to bake, {} baked correctly.".format(timed_out, success))
        elif failed and timed_out:
            print("{} baguettes are failed and the {} others took too long to bake...".format(failed, timed_out))
        elif failed:
            print("All {} baguettes did not bake correctly...".format(failed))
        elif timed_out:
            print("All {} baguettes took too long to bake...".format(timed_out))
        elif success:
            print("All {} are well-baked!".format(success))
        ExitCode.exit(ExitCode(0) if not missing_data else ExitCode.BAKING_MISSING_DATA, ExitCode(0) if not unknown_exception else ExitCode.BAKING_UNKNOWN_EXCEPTION, ExitCode(0) if not timed_out else ExitCode.BAKING_TIMEOUT)
    except SystemExit:
        raise
    except:
        ExitCode.exit()
            




if __name__ == "__main__":
    main()