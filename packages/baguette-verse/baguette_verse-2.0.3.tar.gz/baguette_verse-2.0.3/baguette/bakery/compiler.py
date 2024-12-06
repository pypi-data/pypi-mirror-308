"""
This module contains the compile function which is used to bake baguettes.
"""

from pathlib import Path
from ..filesystem.fluid_path import FluidPath
from ..filesystem.baguette_file import BaguetteFile

__all__ = ["compile", "prepare_and_compile", "BakingTimeout"]





class BakingTimeout(SystemExit):

    """
    This exception means that the compilation (baking) timeout has been reached, causing interpreter exit when raised.
    """





def prepare_and_compile(input_report_path : FluidPath, output_baguette_path : Path):

    """
    Performs both the preparation of the BAGUETTE file with the given report and compiles it on the fly.
    The BaguetteFile must have been initialized with its compilation parameters set.
    """

    from pathlib import Path
    from ..filesystem.baguette_file import BaguetteFile
    from ..filesystem.fluid_path import FluidPath
    import logging
    levels = {
        0 : logging.ERROR,
        1 : logging.WARNING,
        2 : logging.INFO,
        3 : logging.DEBUG
    }
    
    if not isinstance(input_report_path, FluidPath) or not isinstance(output_baguette_path, Path):
        raise TypeError(f"Expected FluidPath and Path, got '{type(input_report_path).__name__}' and '{type(output_baguette_path).__name__}'")
    baguette_file = BaguetteFile(output_baguette_path)

    from ..logger import set_level, logger, get_level
    if get_level() != (l := levels[baguette_file.metadata.compilation_parameters.verbosity]):
        set_level(l)

        logger.debug("Just change worker's verbosity level.")
    
    try:
        logger.debug("Compressing report in BAGUETTE file.")
        baguette_file.report = input_report_path.open()
    except KeyboardInterrupt:
        logger.warning(f"Got a 'KeyboardInterrupt' exception while baking '{baguette_file.path}'. Cleaning up.")
        del baguette_file.report
        return
    except BaseException as e:
        from traceback import print_exc
        logger.warning(f"Got a '{type(e).__name__}' exception while baking '{baguette_file.path}'. Cleaning up.")
        del baguette_file.report
        print_exc()
        return

    compile(baguette_file)





def compile(baguette_file_path : Path | BaguetteFile):

    """
    Compiles a baguette using the BAGUETTE file found at the given path (or a given BaguetteFile not in readonly mode).
    The BaguetteFile must have been initialized with its compilation parameters set.
    """

    from ..filesystem.baguette_file import BaguetteFile
    from pathlib import Path

    if not isinstance(baguette_file_path, Path | BaguetteFile):
        raise TypeError(f"Expected Path or BaguetteFile, got '{type(baguette_file_path).__name__}'")
    if isinstance(baguette_file_path, Path):
        if not baguette_file_path.exists():
            raise FileNotFoundError(f"BAGUETTE file not found: '{baguette_file_path}'")
        if not baguette_file_path.is_file():
            raise FileExistsError(f"Path to BAGUETTE file exists but is not a file: '{baguette_file_path}'")

        baguette_file = BaguetteFile(baguette_file_path)
    
    else:
        if baguette_file_path.readonly:
            raise ValueError("BAGUETTE file opened in readonly mode")
        
        baguette_file = baguette_file_path

    import logging
    levels = {
        0 : logging.ERROR,
        1 : logging.WARNING,
        2 : logging.INFO,
        3 : logging.DEBUG
    }
    
    from ..logger import set_level, logger, get_level
    if get_level() != (l := levels[baguette_file.metadata.compilation_parameters.verbosity]):
        set_level(l)

        logger.debug("Just change worker's verbosity level.")

    try:

        if baguette_file.baked:
            return
        
        from .source.build import Builder
        from .source.config import CompilationParameters, ajust_for_background_color
        from .source import types
        from Boa.parallel.thread import Future, DaemonThread

        if baguette_file.metadata.compilation_parameters.perf:
            from .source.utils import chrono
            chrono.enabled = True
            chrono.auto_report = True

        if not baguette_file.has_report():
            raise FileNotFoundError(f"No report found in BAGUETTE file: '{baguette_file_path}'")

        if baguette_file.metadata.compilation_parameters.skip_data_comparison:
            CompilationParameters.SkipLevenshteinForDataNodes = True
        if baguette_file.metadata.compilation_parameters.skip_diff_comparison:
            CompilationParameters.SkipLevenshteinForDiffNodes = True

        result : Future[bool] = Future()

        def compile_main():
            
            try:
                logger.info("Loading file...")
                b = Builder(baguette_file.report, baguette_file.metadata.compilation_parameters.report_type)
                baguette_file.metadata.compilation_parameters.report_type = b.parser.report_name
                logger.info("Checking color settings...")
                ajust_for_background_color(baguette_file.metadata.compilation_parameters.background_color)
                logger.info("Building graph...")
                b.build()
                logger.info("Analyzing graph...")
                logger.info(f"Got {len(b.graph.vertices)} vertices and {len(b.graph.edges)} edges.")
                logger.info("Saving with pickle")
                baguette_file.baguette = b.graph
                result.set(True)
                logger.info("Done !")
            except BaseException as e:
                result.set_exception(e)

        def death_timer():
            from time import sleep
            from Viper.format import duration
            if baguette_file.metadata.compilation_parameters.timeout < float("inf"):
                logger.info("Death timer thread started. {} remaining.".format(duration(baguette_file.metadata.compilation_parameters.timeout)))
                sleep(baguette_file.metadata.compilation_parameters.timeout)
                logger.error("Death timer reached, about to exit.")
                result.set_exception(BakingTimeout("Baking maxtime reached"))
            else:
                while True:
                    sleep(600)
        
        t1 = DaemonThread(target = compile_main)
        t2 = DaemonThread(target = death_timer)
        t1.start()
        t2.start()
        
        while not result.wait(0.1):
            pass
        result.result()
    
    except BaseException as e:
        from traceback import print_exc, TracebackException
        baguette_file.metadata.compilation_parameters.exception = TracebackException.from_exception(e)
        logger.warning(f"Got a '{type(e).__name__}' exception while baking '{baguette_file.path}'")
        if not isinstance(e, (KeyboardInterrupt, BakingTimeout)):
            print_exc()
    
    finally:
        logger.debug(f"Closing BAGUETTE file at '{baguette_file.path}'")
        baguette_file.close()





del Path, FluidPath, BaguetteFile