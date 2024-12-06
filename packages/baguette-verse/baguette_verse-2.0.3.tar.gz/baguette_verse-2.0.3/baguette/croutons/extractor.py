"""
This module contains the extract function which is used to toast baguettes.
"""

from pathlib import Path
from ..filesystem.baguette_file import BaguetteFile

__all__ = ["extract", "ToastingTimeout"]





class ToastingTimeout(SystemExit):

    """
    This exception means that the extraction (toasting) timeout has been reached, causing interpreter exit when raised.
    """





def extract(baguette_file_path : Path | BaguetteFile):

    """
    Extracts patterns in a BAGUETTE Graph both found in the BAGUETTE file at given path.
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

    from ..logger import set_level, logger
    
    try:

        if baguette_file.toasted:
            return
        
        if not baguette_file.has_baguette():
            if baguette_file.baked:
                raise ValueError("BAGUETTE file was not baked successfully")
            raise ValueError("BAGUETTE file has not been baked yet")
        
        import logging
        levels = {
            0 : logging.ERROR,
            1 : logging.WARNING,
            2 : logging.INFO,
            3 : logging.DEBUG
        }
        
        set_level(levels[baguette_file.metadata.extraction_parameters.verbosity])

        logger.debug("Just change worker's verbosity level.")

        from Boa.parallel.thread import Future, DaemonThread
        from ..bakery.source.graph import Graph

        if baguette_file.metadata.extraction_parameters.perf:
            from ..bakery.source.utils import chrono
            chrono.enabled = True
            chrono.auto_report = True

        result : Future[bool] = Future()

        def extract_main():
            
            try:
                logger.info("Loading baguette...")
                b = baguette_file.baguette

                if not isinstance(b, Graph):
                    raise TypeError("Given file did not contain a Graph object")

                logger.info("Loading necessary MetaGraphs...")
                patterns = baguette_file.patterns

                logger.info("Searching patterns in baguette graph...")

                n_matches = 0
                def match_iterator():
                    nonlocal n_matches
                    for pattern in baguette_file.patterns:
                        pattern_color = pattern.paint_color if baguette_file.metadata.extraction_parameters.paint_color is None else baguette_file.metadata.extraction_parameters.paint_color if baguette_file.metadata.extraction_parameters.paint_color is not False else None
                        if pattern_color:
                            for match in pattern.match_iter(b):
                                match.graph.paint(pattern_color)
                                yield match
                                n_matches += 1
                        else:
                            for match in pattern.match_iter(b):
                                yield match
                                n_matches += 1

                baguette_file.matches = match_iterator()
                logger.info(f"Exported {n_matches} matches to BAGUETTE file.")

                result.set(True)
                logger.info("Done!")
            except BaseException as e:
                result.set_exception(e)

        def death_timer():
            from time import sleep
            from Viper.format import duration
            if baguette_file.metadata.extraction_parameters.timeout < float("inf"):
                logger.info("Death timer thread started. {} remaining.".format(duration(baguette_file.metadata.extraction_parameters.timeout)))
                sleep(baguette_file.metadata.extraction_parameters.timeout)
                logger.error("Death timer reached, about to exit.")
                result.set_exception(ToastingTimeout("Toasting maxtime reached"))
            else:
                while True:
                    sleep(600)
        
        t1 = DaemonThread(target = extract_main)
        t2 = DaemonThread(target = death_timer)
        t1.start()
        t2.start()
        
        while not result.wait(0.1):
            pass
        result.result()
    
    except BaseException as e:
        from traceback import print_exc, TracebackException
        baguette_file.metadata.extraction_parameters.exception = TracebackException.from_exception(e)
        if not isinstance(e, (KeyboardInterrupt, ToastingTimeout)):
            print_exc()

    finally:
        logger.debug(f"Closing BAGUETTE file at '{baguette_file.path}'")
        baguette_file.close()





del Path, BaguetteFile