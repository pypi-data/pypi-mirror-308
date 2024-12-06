"""
A special setuptools script that will add registry keys for the BAGUETTE file format on Windows.
Just a normal declarative script on Linux.
"""

from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop





class WindowsPostInstallScript(install):

    """
    A special installer for associating .bag files with the correct command on windows.
    """

    def run(self):
        install.run(self)
        from sys import platform
        from pathlib import Path
        import baguette
        from baguette.setup.preferences import preferences_dir, global_preferences_dir
        print(f"Creating BAGUETTE preferences directory in '{preferences_dir}'")
        preferences_dir.mkdir(exist_ok=True)
        current_path = Path(baguette.__file__).expanduser().absolute().parent
        print(f"Installation path is '{current_path}'")
        if platform == "win32":
            print("Copying '.ico' file into preferences directory")
            from shutil import copy
            copy(current_path / "data" / "baguette.ico", global_preferences_dir / "baguette.ico")
            print("Registering '.bag' file format into system registry.")
            from baguette.setup.winreg import install_baguette_file_format
            install_baguette_file_format()

class WindowsPostDevelopScript(develop):

    """
    A special (developper) installer for associating .bag files with the correct command on windows.
    """

    def run(self):
        develop.run(self)
        from sys import platform
        from pathlib import Path
        import baguette
        from baguette.setup.preferences import preferences_dir, global_preferences_dir
        print(f"Creating BAGUETTE preferences directory in '{preferences_dir}'")
        preferences_dir.mkdir(exist_ok=True)
        current_path = Path(baguette.__file__).expanduser().absolute().parent
        print(f"Installation path is '{current_path}'")
        if platform == "win32":
            print("Copying '.ico' file into preferences directory")
            from shutil import copy
            copy(current_path / "data" / "baguette.ico", global_preferences_dir / "baguette.ico")
            print("Registering '.bag' file format into system registry.")
            from baguette.setup.winreg import install_baguette_file_format
            install_baguette_file_format()





dependencies = [
    "viper_lib>=1.5.2",
    "boa_lib>=1.2",
    "python-magic; platform_system != 'Windows'",
    "python-magic-bin; platform_system == 'Windows'",
    "Levenshtein",
    "alive-progress>=3.1.5"
]

setup(
    name = 'baguette-verse',
    version = '2.0.3',
    description = "A malware behavioral analysis framework centered around BAGUETTE!",
    author="Vincent Raulin",
    author_email="vincent.raulin@inria.fr",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Affero General Public License v3",
    "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://gitlab.inria.fr/vraulin/baguette-verse',
        'Tracker': 'https://gitlab.inria.fr/vraulin/baguette-verse/-/issues',
    },
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    license_files = ('LICENSE',),
    install_requires = dependencies,
    setup_requires = dependencies,          # Let's not take any risks...
    packages=find_packages(include=["baguette*"]),
    entry_points={
        "console_scripts" : [
            'prepare = baguette.prepare:main',
            'bake = baguette.bake:main',
            'metalib = baguette.metalib:main',
            'toast = baguette.toast:main',

            'baguette = baguette.baguette:main',

            'baguette.prepare = baguette.prepare:main',
            'baguette.bake = baguette.bake:main',
            'baguette.metalib = baguette.metalib:main',
            'baguette.toast = baguette.toast:main',

            'baguette.settings = baguette.setup.__init__:main',
            'baguette.exit_codes = baguette.exit_codes:main',

            'baguette.open = baguette.open:main',

            'baguette.tutorial = baguette.tutorial.scripts:start',
            'baguette.tutorial.reset = baguette.tutorial.scripts:reset',
            'baguette.tutorial.status = baguette.tutorial.scripts:status',
            'baguette.tutorial.help = baguette.tutorial.scripts:help',
            'baguette.tutorial.samples = baguette.tutorial.scripts:copy_reports'

        ]
    },
    cmdclass={
        'install' : WindowsPostInstallScript,
        'develop' : WindowsPostDevelopScript
    }, 
    package_data={
        "baguette" : ["data/*", "setup/unix_open.sh", "bakery/source/parsers/translators/*.json"]
    }
)