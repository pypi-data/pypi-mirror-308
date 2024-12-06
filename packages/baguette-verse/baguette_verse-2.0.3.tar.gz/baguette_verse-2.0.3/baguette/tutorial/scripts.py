"""
This module contains all the functions that the tutorial will call for all steps.
"""

import argparse
import shutil
import textwrap
from pathlib import Path

from .utils import data_filesystem, extract_subfolder, walk_archive, get_state, next_state, set_state, states, create_command_line


def clean_print(text : str):
    w, h = shutil.get_terminal_size()
    for line in text.splitlines():
        print("\n".join(textwrap.wrap(line, w)))


def help():
    clean_print(
"""Throughout this tutorial, you can use:
- 'baguette.tutorial' to move to the next step,
- 'baguette.tutorial.reset' to restart the tutorial, 
- 'baguette.tutorial.status' to know the progress of the tutorial,
- 'baguette.tutorial.help get see this message.
""")


def start():

    match get_state():

        case "not started":
            clean_print("""Welcome to the BAGUETTE tutorial. You will learn how to use BAGUETTE from start to end (without the details).\n
BAGUETTE is a framework to analyze efficiently malware dynamic analysis reports. Indeed, BAGUETTE means Behavioral Analysis Graph Using Execution Traces Towards Explainability.\n""")
            help()
            clean_print("""First you will need a working directory to perform this tutorial. If not already done, create one and continue from this new folder.
To use BAGUETTE, you will first need some report samples. Use 'baguette.tutorial.samples -h' to have some execution report examples.""")

            next_state("not started")

        case "preparing":

            baguette_folder = Path("./Baguette")
            clean_print("Checking the BAGUETTEs you prepared.")

            def check(bpath : Path) -> bool:
                if not bpath.is_dir():
                    return False
                n = 0
                for p in bpath.iterdir():
                    if p.suffix == ".bag" and p.is_file():
                        n += 1
                return bool(n)

            try:
                if not check(baguette_folder):
                    clean_print("I could not find the path in which you prepared your BAGUETTEs. Where is the folder that contains the '.bag' files?")
                    n = 0
                    while not check(baguette_folder) and n < 3:
                        n += 1
                        path = input("> ")
                        try:
                            baguette_folder = Path(path)
                        except:
                            clean_print("That is not a valid path...Try again")
                            continue
                        if not check(baguette_folder):
                            clean_print("That is not an existing folder or it does not contain '.bag' files...Try again")
                    if not check(baguette_folder):
                        clean_print("Look into your file system or restart the tutorial to get some BAGUETTEs!")
                        exit(1)
            except KeyboardInterrupt:
                clean_print("Exiting.")
                exit(1)

            success : list[Path] = []
            failed : list[Path] = []
            other : list[Path] = []
            from ..filesystem import BaguetteFile
            from ..progress import ProgressBar
            files = list(baguette_folder.glob("*.bag"))
            with ProgressBar("Looking at the BAGUETTEs you prepared") as bar:
                bar.total = len(files)
                for p in files:
                    if p.is_file():
                        bag = BaguetteFile(p, mode='r')
                        if not bag.has_report():
                            failed.append(p)
                        else:
                            success.append(p)
                        bag.close()
                    else:
                        other.append(p)
                    bar.current += 1
            
            if success and not failed:

                clean_print(f"I found {len(success)} well-prepared BAGUETTEs!")

            elif success:

                clean_print(f"I found {len(success)} well-prepared BAGUETTEs and {len(failed)} failed. You might want to investigate those later.")

            elif failed:

                clean_print(f"All {len(failed)} BAGUETTEs were not well-prepared. Restart the tutorial now!")
                exit(1)
            
            else:

                clean_print("I found no BAGUETTE files. Restart the tutorial now!")
                exit(1)

            if not failed and not other:
                args = [f"'{baguette_folder}/*.bag'"]
            else:
                args = [f'{p}' for p in success]
            
            clean_print(f"""
You may now bake those BAGUETTEs. To do so, use the 'bake' command.
You can type 'bake -h' to learn more about the baking process. Note that 'bake' can take care of the preparation step using the '--raw' option.
For now, use this:
{create_command_line("bake", *args)}
""")
            next_state("preparing")

        case "baking":
            baguette_folder = Path("./Baguette")
            clean_print("Checking the BAGUETTEs you baked.")

            def check(bpath : Path) -> bool:
                if not bpath.is_dir():
                    return False
                n = 0
                for p in bpath.iterdir():
                    if p.suffix == ".bag" and p.is_file():
                        n += 1
                return bool(n)

            try:
                if not check(baguette_folder):
                    clean_print("I could not find the path in which you made your BAGUETTEs. Where is the folder that contains the '.bag' folders?")
                    n = 0
                    while not check(baguette_folder) and n < 3:
                        n += 1
                        path = input("> ")
                        try:
                            baguette_folder = Path(path)
                        except:
                            clean_print("That is not a valid path...Try again")
                            continue
                        if not check(baguette_folder):
                            clean_print("That is not an existing folder or it does not contain '.bag' folders...Try again")
                    if not check(baguette_folder):
                        clean_print("Look into your file system or restart the tutorial to get some BAGUETTEs!")
                        exit(1)
            except KeyboardInterrupt:
                clean_print("Exiting.")
                exit(1)

            success : list[Path] = []
            failed : list[Path] = []
            other : list[Path] = []
            from ..filesystem import BaguetteFile
            from ..progress import ProgressBar
            files = list(baguette_folder.glob("*.bag"))
            with ProgressBar("Looking at the BAGUETTEs you baked") as bar:
                bar.total = len(files)
                for p in files:
                    if p.is_file():
                        bag = BaguetteFile(p, mode='r')
                        if not bag.has_baguette():
                            failed.append(p)
                        else:
                            success.append(p)
                        bag.close()
                    else:
                        other.append(p)
                    bar.current += 1
            
            if success and not failed:

                clean_print(f"I found {len(success)} well-baked BAGUETTEs!")

            elif success:

                clean_print(f"I found {len(success)} well-baked BAGUETTEs and {len(failed)} failed. You might want to investigate those later.")

            elif failed:

                clean_print(f"All {len(failed)} BAGUETTEs were not well-baked. Restart the tutorial now!")
                exit(1)
            
            else:

                clean_print("I found no BAGUETTE files. Restart the tutorial now!")
                exit(1)
            
            clean_print("""
Let's talk a bit about those BAGUETTE files. A BAGUETTE file (.bag) is a file format that holds many useful objects to work on an execution report:
- by using the 'prepare' command, we stored each report in a corresponding BAGUETTE file.
- by using the 'bake' command, we just compiled this report into a behavioral graph (the BAGUETTE Graph) and stored it in this file too.
- by using the next commands you will discover that we will also store some behavioral queries.
""")

            chosen_baguette = success[0]
            clean_print(f"""
Also, an important point: BAGUETTE files are executable! By running one, you will interact with it in many ways.
(Don't panic, running the executable 'my_baguette.bag [...]' is almost equivalent to 'baguette.open my_baguette.bag [...]'.)
For instance, just running the BAGUETTE will open an interactive prompt with the BAGUETTE file loaded. Try it:

{create_command_line(chosen_baguette)}

You should get something like that:
BAGUETTE Interactive Prompt. Variable 'bag' holds the opened BAGUETTE file.
Most BAGUETTE packages are also loaded. Use dir() and help() to find out more.
>>> help(bag)
Help on BaguetteFile in module baguette.filesystem.baguette_file object:
...
>>> bag.baguette
<baguette.bakery.source.graph.FrozenGraph object at 0x0000024D215EB9D0>  # The actual BAGUETTE Graph itself

You can also give some commands to this executable:

{create_command_line(chosen_baguette, "gephi")}         # Opens Gephi to visualize the BAGUETTE Graph
{create_command_line(chosen_baguette, "--help")}        # To see all the capabilities of this executable!

Good luck! And use 'baguette.tutorial' to learn about toasting!""")

            next_state("baking")

        case "baked":

            clean_print("""Now that you have baked some BAGUETTEs, it is time to learn about MetaGraphs!

Since BAGUETTE has a well-defined graph type structure, you can use it to define patterns.
Put simply, MetaGraphs are pattern graphs. Indeed, they are made of MetaVertices, MetaEdges and MetaArrows, which are just like normal Vertices, Edges and Arrows, except that they allow you to put constrains on types to match real vertices, edges or arrows.

For example, 'MetaVertex[File]' would mean 'Match a vertex which type is "File"'.
If you have two MetaVertices MV1 and MV2, then 'MetaArrow(MV1, MV2)[HasChildProcess]' would mean 'Match an arrow between the two vertices you already matched for MV1 and MV2, which type should be \"HasChildProcess\"'.

With such a syntax, you can build MetaGraphs using the 'metalib'. It is a script that can be launched without parameters which will start a Python interactive prompt with the environment necessary to work on MetaGraphs. Use 'dir()' to list all the resources available in the environment and 'help(resource)' to learn more about any of those.

In the metalib, we could declare a simple MetaGraph using a few commands:
>>> MG = MetaGraph()
>>> MG.File = MetaVertex[filesystem.File]
>>> MG.Directory = MetaVertex[filesystem.Directory]
>>> MG.Contains = MetaEdge(MG.Directory, MG.File)[filesystem.contains]
>>> save(MG, "dile_in_directory")

Note that in BAGUETTE, all the Vertex, Edge and Arrow subclasses are organized in behavioral packages, such as 'filesystem'. Others can be listed with 'behavioral_packages()'.
Remember, all the information you want can be found using Python 'dir' function (to enumerate your environment) and 'help' to find information about the available resources.

For this step of the tutorial, launch the metalib using the command 'metalib' and create a metagraph of your choice and save it under the name you want.
You can use 'metalib -h' to see all the capabilities of this command.""")

            next_state("baked")

        case "metalib":

            clean_print("You should now have created at least one MetaGraph. Checking...")

            from ..croutons.metalib.utils import entries, load
            
            if not entries():
                clean_print("I could not find any MetaGraph in the metalib! Did you save your MetaGraph before leaving? COme back when you see your MetaGraph when using 'entries()' in the metalib.")
                exit(1)
            
            if len(entries()) == 1:
                clean_print(f"I found a MetaGraph named '{entries()[0]}'.")
                chosen_metagraph = entries()[0]
            
            elif len(entries()) < 10:
                clean_print("I found multiple MetaGraphs. Which want do you want to use?")
                choices = {letter : name for letter, name in zip("abcdefghij", entries())}
                for l, n in choices.items():
                    clean_print(f"\t{l}) '{n}'")
                try:
                    c = input("Write the letter of your choice > ")
                    n = 0
                    while c not in choices and n < 3:
                        clean_print(f"Could not understand your choice : '{c}'. Try again:")
                        n += 1
                        c = input("Write the letter of your choice > ")
                    if c not in choices:
                        clean_print("Could not get a valid input. Giving up.")
                        exit(1)
                except KeyboardInterrupt:
                    clean_print("Exiting.")
                    exit(1)
                
                chosen_metagraph = choices[c]
                clean_print(f"You've chosen the MetaGraph '{chosen_metagraph}'. Loading it...")
            
            else:
                clean_print("There are many MetaGraphs!")
                try:
                    c = input("Write the name of your MetaGraph > ")
                    n = 0
                    while c not in entries() and n < 3:
                        clean_print(f"Could not find your choice : '{c}'. Try again:")
                        n += 1
                        c = input("Write the name of your MetaGraph > ")
                    if c not in entries():
                        clean_print("Could not get a valid input. Giving up.")
                        exit(1)
                except KeyboardInterrupt:
                    clean_print("Exiting.")
                    exit(1)

                chosen_metagraph = c
                clean_print(f"You've chosen the MetaGraph '{chosen_metagraph}'. Loading it...")
            
            MG = load(chosen_metagraph)

            if len(MG.vertices) == 0:
                clean_print("That's lazy. You made an empty MetaGraph. It won't do much...")
            elif len(MG.vertices) == 1 and len(MG.edges) == 0:
                clean_print("That's lazy. You made the most minimalistic MetaGraph...")
            elif len(MG.vertices) < 3:
                clean_print(f"Ok, nice MetaGraph. Got {len(MG.vertices)} vertice{'s' if len(MG.vertices) > 1 else ''} and {len(MG.edges)} edge{'s' if len(MG.edges) > 1 else ''}/arrow{'s' if len(MG.edges) > 1 else ''}.")
            else:
                clean_print(f"That's a big MetaGraph! Got {len(MG.vertices)} vertice{'s' if len(MG.vertices) > 1 else ''} and {len(MG.edges)} edge{'s' if len(MG.edges) > 1 else ''}/arrow{'s' if len(MG.edges) > 1 else ''}!")
            
            clean_print(f"""
To search for matches of this MetaGraph in the BAGUETTEs you made, you need to affect them to the BAGUETTE files and then toast them.
To write them to a BAGUETTE file, you can use "metalib decorate <your BAGUETTE file(s)> --pattern '{chosen_metagraph}'".
This will actually affect the selected MetaGraph patterns from the library to the 'patterns' property of BaguetteFiles. Use 'metalib decorate -h' and 'help(BaguetteFile)' (in an interactive interpreter) to learn more.
Then you need to use the 'toast' command. This will actually perform the pattern search across your BAGUETTE files:
{create_command_line("toast", "<your BAGUETTE folder>", "--paint", "red")}

Note that you could have also decorated your BAGUETTE files using 'metalib export' and 'toast --patterns'.
""")

            next_state("metalib")

        case "toasting":

            clean_print("Examining your toasts...")

            from pickle import load

            from ..bakery.source.graph import Graph

            baguette_folder = Path("./Baguette")

            def check(bpath : Path) -> bool:
                if not bpath.is_dir():
                    return False
                n = 0
                for p in bpath.iterdir():
                    if p.suffix == ".bag" and p.is_file():
                        n += 1
                return bool(n)

            try:
                if not check(baguette_folder):
                    clean_print("I could not find the path in which you made your BAGUETTEs. Where is the folder that contains the '.bag' folders?")
                    n = 0
                    while not check(baguette_folder) and n < 3:
                        n += 1
                        path = input("> ")
                        try:
                            baguette_folder = Path(path)
                        except:
                            clean_print("That is not a valid path...Try again")
                            continue
                        if not check(baguette_folder):
                            clean_print("That is not an existing folder or it does not contain '.bag' folders...Try again")
                    if not check(baguette_folder):
                        clean_print("Look into your file system or restart the tutorial to get some BAGUETTEs!")
                        exit(1)
            except KeyboardInterrupt:
                clean_print("Exiting.")
                exit(1)

            success : list[Path] = []
            failed : list[Path] = []
            other : list[Path] = []
            from ..filesystem import BaguetteFile
            from ..progress import ProgressBar
            files = list(baguette_folder.glob("*.bag"))
            with ProgressBar("Looking at the BAGUETTEs you toasted") as bar:
                bar.total = len(files)
                for p in files:
                    if p.is_file():
                        bag = BaguetteFile(p, mode='r')
                        if not bag.has_matches():
                            failed.append(p)
                        else:
                            success.append(p)
                        bag.close()
                    else:
                        other.append(p)
                    bar.current += 1
            
            if success and not failed:

                clean_print(f"I found {len(success)} well-toasted BAGUETTEs!")

            elif success:

                clean_print(f"I found {len(success)} well-toasted BAGUETTEs and {len(failed)} failed. You might want to investigate those later.")

            elif failed:

                clean_print(f"All {len(failed)} BAGUETTEs were not well-toasted. Restart the tutorial now!")
                exit(1)
            
            else:

                clean_print("I found no BAGUETTE files. Restart the tutorial now!")
                exit(1)
            
            empty_found = False
            interesting_found = False
            from ..croutons.metalib.utils import index
            metalib = index()
            for bag_path in success:
                bag = BaguetteFile(bag_path, mode = "r")
                if bag.matches is None:
                    raise RuntimeError("Validated BAGUETTE has no matches.")
                if len(bag.matches) == 0:
                    empty_found = True
                    clean_print(f"\nThe MetaGraphs you defined did not have any match in the BAGUETTE '{bag_path.name}'. That means the corresponding behavioral patterns are not relevant for this malware sample.")
                elif not interesting_found:
                    interesting_found = True
                    clean_print(f"\nThe BAGUETTE at '{bag_path.name}' had at least one match. To be more precise, it had matches for the following MetaGraph{('s' if len(bag.matches.patterns) > 1 else '')}:")
                    for mg in bag.matches.patterns:
                        if mg in metalib:
                            clean_print(f"\t - for MetaGraph '{metalib[mg]}' : {len(bag.matches[mg])} matches.")
                        else:
                            clean_print(f"\t - for an unknown MetaGraph : {len(bag.matches[mg])} matches.")
                    clean_print(f"This means the MetaGraph{('s' if len(bag.matches.patterns) > 1 else '')} you match relevent behavior for this sample.")
                if interesting_found and empty_found:
                    break
            
            clean_print(f"""
You now know how to use the basic functionalities of BAGUETTE.
To learn further, you will need to dive into the very dense documentation of BAGUETTE. To do so, simply use '-h/--help' on command line tools or use the 'help()' function in an interactive Python interpreter on any class/module/package of BAGUETTE.

Bon voyage!""")

            next_state("toasting")

        case "finished":

            clean_print("That's it! You completed the tutorial! Get baking now!")

        case x:

            if x not in states():
                clean_print("How did you get there? You broke the tutorial. Use 'baguette.tutorial.reset' now!")
            else:
                status()

def reset():
    clean_print("Resetting BAGUETTE tutorial.")
    set_state("not started")


def status():
    clean_print(f"Tutorial is currently at step : '{get_state()}' : {states()[get_state()]}")


def copy_reports():

    from ..progress import ProgressBar

    parser = argparse.ArgumentParser("baguette.tutorial.samples", description="This script will copy report examples (BAGUETTE input files) to the given destination folder.")

    parser.add_argument("destination", type=Path, default=Path("."), nargs="?", help="The path to the destination folder in which to copy report folders. Defaults to '.'.")

    args = parser.parse_args()

    if get_state() != "fetching samples":
        clean_print("Warning : fetching Cuckoo report samples in the wrong step of tutorial.")

    pth : Path = args.destination

    if pth.exists() and not pth.is_dir():
        parser.error("given destination path exists and is not a directory.")
    pth.mkdir(parents=True, exist_ok=True)

    reports_dir = data_filesystem / "reports"
    if not reports_dir.exists():
        raise FileNotFoundError("Could not find the report folder in the data archive! Check your BAGUETTE installation.")
    if not reports_dir.is_dir():
        raise FileExistsError("Report folder is not a folder in the data archive! Check you BAGUETTE installation.")

    dirs : "list[Path]" = []
    size = len(list(walk_archive(reports_dir, leaves_only=True)))
    with ProgressBar("Extracting execution reports") as bar:
        bar.total = size - 1
        for p in extract_subfolder(reports_dir, pth):
            dirs.append(p)
            if p.is_file():
                bar.current += 1

    if pth.resolve() == Path.cwd():
        clean_print("Playground dataset available in current folder.")
    else:
        clean_print(f"Playground dataset available in '{pth}'")

    clean_print("""
The next step is to prepare the BAGUETTE files with those reports. To do so, use the 'prepare' command.
You can use 'prepare -h' to learn ALL the options of prepare.""")

    report_folders = {p.parent for p in dirs if p.is_file()}

    if not report_folders:
        clean_print("Could not find the extracted report folders...")
        exit(1)

    clean_print(f"""
For example, to prepare the newly made reports into the folder './Baguette', use:
{create_command_line("prepare", *(f"'{pi}/*'" for pi in report_folders), "./Baguette")}
""")
    
    clean_print("Once this is done, use again 'baguette.tutorial'.")

    next_state("fetching samples")