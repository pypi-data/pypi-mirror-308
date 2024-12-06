"""
This is a *magic* script create an empty BAGUETTE file. Use -h/--help for usage.
"""





def main():
    """
    Command line function to bake execution report(s). Use -h/--help for more info.
    """

    import logging
    from .logger import logger, set_level
    from .filesystem import BaguetteFile
    from .filesystem.fluid_path import FluidPath
    from .progress import ProgressBar
    from .exit_codes import ExitCodeParser, ExitCode
    from pathlib import Path
    from typing import Literal

    parser = ExitCodeParser(
        "new",
        description = 'Creates empty BAGUETTE files or wipes clean existing ones.',
        add_help = False,
        conflict_handler = 'resolve',
        )

    def writable_fluid_path(arg : str) -> FluidPath:
        return FluidPath(arg, allow_zip=False)

    parser.add_argument("baguettes", nargs="+", type=writable_fluid_path, help="The paths to the BAGUETTE files to create or clean. Supports wildcards.")
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

    abstract_baguette_paths : list[FluidPath] = args.baguettes
    baguette_paths : list[Path] = []
    for p in abstract_baguette_paths:
        baguette_paths.extend(Path(str(pi)) for  pi in p.expand())
    for p in baguette_paths:
        if p.exists() and not p.is_file():
            parser.error(f"output file exists and is not a file: '{p}'")
    
    logger.info(f"Creating BAGUETTE {len(baguette_paths)} files.")
    try:
        with ProgressBar("Creating empty BAGUETTE files") as bar:
            bar.total = len(baguette_paths)
            for p in baguette_paths:
                p.parent.mkdir(exist_ok=True, parents=True)
                bag = BaguetteFile(p, mode = "w")
                bag.close()
                bar.current += 1
    except:
        ExitCode.exit()





if __name__ == "__main__":
    main()