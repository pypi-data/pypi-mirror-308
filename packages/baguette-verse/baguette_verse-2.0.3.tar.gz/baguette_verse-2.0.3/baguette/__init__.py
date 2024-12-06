"""
This is the BAGUETTE framework. BAGUETTE stands for Behavioral Analysis Graph Using Execution Traces Towards Explanability.
BAGUETTE is a heterogeneous graph data structure used to represent the behavior of malware samples.
To learn how to use it quickly, simply type 'baguette.tutorial' in your terminal.
"""

__all__ = ["bakery", "croutons", "logger"]

from .filesystem import *
from .bakery.source.graph import *
from .bakery.source.types import *
from .croutons.source.metagraph import *