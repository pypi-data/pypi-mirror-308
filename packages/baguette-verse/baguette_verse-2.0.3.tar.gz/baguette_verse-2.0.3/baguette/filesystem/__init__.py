"""
A package that defines some very complex data management classes to be able to read and write the BAGUETTE file format.
"""

__all__ = ["BaguetteFile", "is_baguette_file"]

from .baguette_file import BaguetteFile, is_baguette_file