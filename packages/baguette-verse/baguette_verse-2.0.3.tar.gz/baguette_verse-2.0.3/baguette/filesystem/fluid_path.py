"""
A useful way to represent paths in many different ways. These path can contain wildcards and even look into zip files!
"""

from .abc import BytesReadable

__all__ = ["FluidPath"]





class FluidPath:

    """
    A class to transform path-like strings into one or multiple similar fluid-paths, exploring the file system if wildcards are present and even looking into zip files.
    Also multiple paths can be separated by ';'.
    """

    from sys import platform
    if platform == "win32":
        from fnmatch import fnmatchcase as fnmatch
    else:
        from fnmatch import fnmatch
    from os import sep as __sep
    from pathlib import Path as __Path
    from zipfile import ZipFile as __ZipFile, is_zipfile
    __fnmatch = staticmethod(fnmatch)
    __is_zipfile = staticmethod(is_zipfile)
    del fnmatch, is_zipfile, platform

    def __init__(self, path : str, *, allow_zip : bool = True, allow_wildcards : bool = True, allow_multiple_files : bool = True) -> None:
        if not isinstance(path, str):
            raise TypeError(f"Expected str, got '{type(path).__name__}'")
        self.__path = path
        self.__allow_zip = allow_zip
        self.__allow_wildcards = allow_wildcards
        self.__allow_multiple_files = allow_multiple_files

    def __str__(self) -> str:
        return self.__path
    
    def __repr__(self) -> str:
        return f"FluidPath('{self.__path}')"

    def expand(self) -> list["FluidPath"]:
        """
        Expands the FluidPath, returning a list of singular FluidPaths. Returns [self] if it is already singular.
        """
        if ';' in self.__path and self.__allow_multiple_files:
            l = []
            for sub_part in self.__path.split(";"):
                l.extend(FluidPath(sub_part, allow_zip=self.__allow_zip, allow_wildcards=self.__allow_wildcards, allow_multiple_files=self.__allow_multiple_files).expand())
            return l
        
        parts = FluidPath.__Path(self.__path).parts
        path = FluidPath.__Path(parts[0])
        i = 1
        while path.exists() and i < len(parts):        # Here we discover the already existing parts.
            path /= parts[i]
            i += 1
        
        if path.exists():
            return [self]

        existing = FluidPath.__Path(*parts[:i - 1])
        if existing.is_file():
            if FluidPath.__is_zipfile(existing) and self.__allow_zip:        # Let's explore the zip file
                zip_file = FluidPath.__ZipFile(existing)
                zip_pattern = f"{FluidPath.__sep}".join(parts[i - 1:])
                return [FluidPath(f"{existing}{FluidPath.__sep}{p}", allow_zip=self.__allow_zip, allow_wildcards=self.__allow_wildcards, allow_multiple_files=self.__allow_multiple_files) for p in zip_file.namelist() if FluidPath.__fnmatch(p, zip_pattern)]
            return []       # The node before was an endpoint

        l = []
        if self.__allow_wildcards:
            for p in existing.glob(parts[i - 1]):       # Let's explore the next eventual wildcard
                l.extend(FluidPath(str(FluidPath.__Path(p, *parts[i:])), allow_zip=self.__allow_zip, allow_wildcards=self.__allow_wildcards, allow_multiple_files=self.__allow_multiple_files).expand())
        return l
    
    @property
    def singular(self) -> bool:
        """
        True if the file actually expands to a singular end point.
        """
        return len(self.expand()) == 1

    def open(self) -> BytesReadable:
        """
        If the FluidPath is singular and is a file, returns a readable binary stream to the file.
        """
        selfs = self.expand()
        if len(selfs) != 1:
            raise ValueError(f"Non singular FluidPath: {self}")
        self = selfs[0]
        parts = FluidPath.__Path(self.__path).parts
        path = FluidPath.__Path(parts[0])
        i = 1
        while path.exists() and i < len(parts):        # Here we discover the already existing parts.
            path /= parts[i]
            i += 1
        
        if path.exists():
            return path.open("rb")
        
        existing = FluidPath.__Path(*parts[:i - 1])
        if existing.is_file():
            if FluidPath.__is_zipfile(existing) and self.__allow_zip:        # Let's explore the zip file
                zip_file = FluidPath.__ZipFile(existing)
                zip_pattern = f"{FluidPath.__sep}".join(parts[i - 1:])
                files = [p for p in zip_file.namelist() if FluidPath.__fnmatch(p, zip_pattern)]
                if len(files) == 1:
                    return zip_file.open(files[0], "r")
        raise RuntimeError(f"Cannot read from FluidPath: {self}")





del BytesReadable