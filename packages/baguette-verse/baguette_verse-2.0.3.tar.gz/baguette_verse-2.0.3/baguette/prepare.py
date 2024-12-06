"""
This is a *magic* script to prepare BAGUETTEs for baking. Use -h/--help for usage.
"""

from pathlib import Path
from .filesystem.fluid_path import FluidPath





def prepare_single_baguette(input_path : FluidPath, output_path : Path, report_type : str | None) -> bool:
    """
    Prepares a single BAGUETTE file at output_path from the report at input_path.
    """
    try:
        from .filesystem import BaguetteFile
        b = BaguetteFile(output_path)
        if report_type is not None:
            b.metadata.compilation_parameters.report_type = report_type
        b.report = input_path.open()
        return True
    except KeyboardInterrupt:
        return False
    except:
        from traceback import print_exc
        print_exc()
        return False





def main():
    """
    Command line function to prepare execution report(s). Use -h/--help for more info.
    """
    
    import logging

    from .logger import logger, set_level
    set_level(logging.ERROR)

    from pathlib import Path
    from os import environ
    from multiprocessing import Process
    from threading import Lock
    from typing import Literal
    from Boa.parallel.thread import DaemonThread

    from .filesystem import BaguetteFile
    from .filesystem.fluid_path import FluidPath
    from .bakery.source.parsers import parsers
    from .progress import ProgressBar
    from .exit_codes import ExitCode, ExitCodeParser

    logger.info("Setting up argument parser")

    parser = ExitCodeParser(
        "prepare",
        description = 'Prepares execution reports for baking, creating unbaked BAGUETTE files.',
        add_help = True,
        conflict_handler = 'resolve',
        epilog="""
        Note that this help changes depending if the environment variables 'BAGUETTE_REPORTS' and 'BAGUETTE_BAGS' are set.
        Both holds paths to directories with respectively all the execution reports or the BAGUETTE files.
        """
        )
        
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

    def pool_size(arg : str) -> int:
        """
        Transforms a numeric argument in a number of process to use as a process pool.
        It can be absolute, negative (relative to the number of CPUs) or proportion greater than 0.
        """
        from os import cpu_count
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

    if "BAGUETTE_REPORTS" in environ:
        parser.add_argument("--reports", "-r", type=FluidPath, action="extend", help="The path(s) to the input execution report(s) to bake into a BAGUETTE file. Accepts wildcards and can look into zip files. Defaults to environment variable 'BAGUETTE_REPORTS'. Parameter '--raw' changes its behavior.")
    else:
        parser.add_argument("reports", type=FluidPath, nargs="+", help="The path(s) to the input execution report(s) to bake into a BAGUETTE file. Accepts wildcards and can look into zip files. Would default to environment variable 'BAGUETTE_REPORTS' if it was set. Parameter '--raw' changes its behavior.")
    if "BAGUETTE_BAGS" in environ:
        parser.add_argument("--output", "-o", type=output_folder_matcher, default=None, help="The output folder where all the BAGUETTE files will be put into. Defaults to environment variable 'BAGUETTE_BAGS'. Parameter '--raw' changes its behavior.")
    else:
        parser.add_argument("output", type=output_folder_matcher, help="The output folder where all the BAGUETTE files will be put into. Would default to environment variable 'BAGUETTE_BAGS' if it was set. Parameter '--raw' changes its behavior.")
    parser.add_argument("--pool", "--ncpus", type=pool_size, default=pool_size("0.5"), help="The size of the process pool to use to prepare BAGUETTE files in parallel.")
    parser.add_argument("--report-type", "--report-format", "-t", choices=[p.report_name for p in parsers], default=None, help="The type of execution report to write in the BAGUETTE file. Not necessary.")
    parser.add_argument("--verbosity", "-v", action="count", default=0, help="Increases the verbosity of the output.")

    args = parser.parse_args()

    levels = {
        0 : logging.ERROR,
        1 : logging.WARNING,
        2 : logging.INFO,
        3 : logging.DEBUG
    }
    verbosity : Literal[0, 1, 2, 3] = min(3, args.verbosity)
    set_level(levels[verbosity])

    logger.info("Arguments parsed. Analyzing I/O arguments.")

    abstract_input_files : list[FluidPath] = args.reports
    if not abstract_input_files and "BAGUETTE_REPORTS" in environ:
        logger.debug("Setting input path(s) from environment variable.")
        abstract_input_files.append(FluidPath(str(Path(environ["BAGUETTE_REPORTS"], "*"))))
    input_files : list[FluidPath] = []
    logger.debug("Expanding input paths.")
    for p in abstract_input_files:
        input_files.extend(p.expand())

    logger.debug("Generating output paths.")
    output_directory : Path | None = args.output
    if output_directory is None:
        output_directory = Path(environ["BAGUETTE_BAGS"])
    output_files = [output_directory / f"{Path(str(p)).stem}.bag" for p in input_files]
    work = [(pi, po) for pi, po in zip(input_files, output_files)]
    report_type : str | None = args.report_type

    lock = Lock()
    failed, success = 0, 0

    def execute_single_job() -> bool:
        nonlocal failed, success
        with lock:
            if not work:
                return False
            input_path, output_path = work.pop()
        proc = Process(target=prepare_single_baguette, args=(input_path, output_path, report_type), daemon=True)
        try:
            logger.debug(f"New job started for input '{input_path}'.")
            proc.start()
            proc.join()
            ok = output_path.is_file() and BaguetteFile(output_path, mode = "r").has_report()
            success += ok
            return ok
        except KeyboardInterrupt:
            proc.kill()
            return False
        except:
            failed += 1
            return True
        finally:
            bar.current += 1
            logger.debug(f"Job for input '{input_path}' finished.")

    def executor():
        while execute_single_job():
            pass
    
    threads : list[DaemonThread] = []
    try:
        logger.debug("Preparing multiprocessing pool.")
        with ProgressBar("Preparing BAGUETTE files") as bar:
            bar.total = len(work)
            for _ in range(args.pool):
                t = DaemonThread(target = executor)
                t.start()
                threads.append(t)

            logger.info("All workers started. Awaiting results.")
            for t in threads:
                t.join()

        logger.info("All jobs finished. Printing results.")
        
        if failed and success:
            print("{} failed jobs, {} BAGUETTEs prepared correctly.".format(failed, success))
        elif failed:
            print("All {} BAGUETTEs were not prepared correctly.".format(failed))
        elif success:
            print("All {} are well-prepared!".format(success))
        ExitCode.exit(ExitCode(0) if not failed else ExitCode.PREPARING_EXCEPTION)
    except SystemExit:
        raise
    except:
        if failed and success:
            print("{} failed jobs, {} BAGUETTEs prepared correctly.".format(failed, success))
        elif failed:
            print("All {} BAGUETTEs were not prepared correctly.".format(failed))
        elif success:
            print("All {} are well-prepared!".format(success))
        ExitCode.exit()





del Path, FluidPath
if __name__ == "__main__":
    main()