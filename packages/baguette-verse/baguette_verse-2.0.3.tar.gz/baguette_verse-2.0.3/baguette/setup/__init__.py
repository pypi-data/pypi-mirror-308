"""
This package holds some tools for seting up BAGUETTE properly.
"""

def main():

    from argparse import ArgumentParser
    from pathlib import Path
    from sys import platform

    parser = ArgumentParser("baguette.settings", description="A command line tool to list, get and set all the settings available for BAGUETTE. Without arguments, lists all the setting with their values. With one of the following arguments, sets them.")

    parser.add_argument("--path-to-gephi", type=Path, required=False, default=None, help="The path to the Gephi executable. This is required to visualize BAGUETTE Graphs. Get it here: https://gephi.org/users/download/")

    if platform == "win32":
        win_reg_setup = parser.add_mutually_exclusive_group()
        win_reg_setup.add_argument("--install-baguette-file-extension", action="store_true", help="If this flag is set, performs the installation of the BAGUETTE file format (.bag) in Windows for the current user.")
        win_reg_setup.add_argument("--remove-baguette-file-extension", action="store_true", help="If this flag is set, removes the BAGUETTE file format (.bag) from Windows for the current user.")

    args = parser.parse_args()


    setting = False


    if isinstance((new_path := args.path_to_gephi), Path):
        setting = True
        from .preferences import save_gephi_path
        save_gephi_path(new_path)
    
    if platform == "win32":
        if args.install_baguette_file_extension:
            print("Installing BAGUETTE file format (.bag) into user's registry.")
            from .winreg import install_baguette_file_format
            install_baguette_file_format()
        
        if args.remove_baguette_file_extension:
            print("Removing BAGUETTE file format (.bag) from user's registry.")
            from .winreg import remove_baguette_file_format
            remove_baguette_file_format()

    if not setting:
        from .preferences import get_gephi_path
        path_to_gephi : Path | None = get_gephi_path()
        print("Here is the current BAGUETTE configuration:")
        print(f"\t--path-to-gephi : {path_to_gephi}")