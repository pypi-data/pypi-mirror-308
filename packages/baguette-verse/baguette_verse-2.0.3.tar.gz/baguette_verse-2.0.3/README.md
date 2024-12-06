# BAGUETTE-VERSE

This is the BAGUETTE framework. BAGUETTE stands for **Behavioral Analysis Graph Using Execution Traces Towards Explanability**.
BAGUETTE is a **heterogeneous graph** data structure used to represent the **behavior of malware samples**.

The BAGUETTE-VERSE is a framework to build and analyze BAGUETTE graphs. 

BAGUETTE requires Python >= 3.12 as well as a few Python modules: viper-lib, boa-lib, alive-progress, python-magic and Levenshtein. You can install all these dependencies by hand, but the easiest way is just to use [`pip`](https://pypi.org/project/baguette-verse/) in the Python installation you want to use:

```$ pip install baguette-verse```

BAGUETTE is a pure Python project, meaning that a BAGUETTE graph is a Python data structure and for now can only be manipulated using the Python interface described below. Please note BAGUETTE is released in the framework of GNU AFFERO GENERAL PUBLIC LICENSE. If you find BAGUETTE package useful in yoru research, please consider citing

**Vincent Raulin, Pierre-François Gimenez, Yufei Han, Valérie Viet Triem Tong. BAGUETTE: Hunting for Evidence of Malicious Behavior in Dynamic Analysis Reports. SECRYPT 2023 - 20th International conference on security and cryptography, Jul 2023, Rome, Italy. pp.1-8. ⟨hal-04102144⟩**

If you want to learn BAGUETTE interactively, once installed, you can just run this command to start the tutorial:

```$ baguette.tutorial```

## Bakery

**Bakery** is the package used to bake (compile) BAGUETTE graphs. For now, BAGUETTEs can only be made from Cuckoo execution reports. From that, the baker will create a BAGUETTE file:
Inside of a ".bag" file and at this point, you may find :
- the original execution report under the "report" attribute,
- the BAGUETTE graph itself, under the "baguette" attribute,

The process of baking a baguette is done throught the 'bake' command:

```
$ bake --help
usage: bake [--raw] [--help] [--pool POOL] [--timeout TIMEOUT] [--report-type {cuckoo}]
            [--filters [{injected_threads_only,modified_registry_only,no_data_nodes,no_handle_nodes,no_simple_imports,significant_call_only,significant_processes_only} ...]] [--idempotent] [--background BACKGROUND] [--verbosity]   
            [--perf] [--skip-data-comparison] [--skip-diff-comparison]
            baguettes [baguettes ...]

Bakes execution reports into BAGUETTE Graphs.
[...]

$ ls
sample.json
$ bake --raw sample.json .
Baking BAGUETTE files |████████████████████████████████████████| 1/1 [100%] in 1:26.7 (0.01/s)
All 1 are well-baked!
$ ls
sample.bag
sample.json
```

Use the help to see all the options of this command and have more information.

BAGUETTE graphs are **heterogeneous graphs**, meaning that their vertices, edges and arrows all have **types** (actual Python classes). To explore the possiblities of these graphs, you can list all these classes from the package `bakery.source.types.utils`. Just open an interactive Python interpreter, import them and explore!
```
>>> from baguette.bakery.source.utils import *

>>> dir()
['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'baguette_structure', 'behavioral_packages', 'relation_types', 'relations', 'types']

>>> packages = behavioral_packages()

>>> packages.keys()
dict_keys(['data', 'execution', 'filesystem', 'imports', 'network', 'registry'])

>>> dir(packages["execution"])
['Call', 'FollowedBy', 'HasChildProcess', 'HasFirstCall', 'HasThread', 'InjectedThread', 'NextSignificantCall', 'Process', 'Runs', 'StartedProcess', 'StartedThread', 'Thread', 'UsesAsArgument', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__proc__', '__spec__', 'entities', 'integration', 'logger', 'relations', 'utils']

>>> {v.__name__ for v in types()}     # Lists all Vertex classes names
{'Thread', 'Key_DWORD_LITTLE_ENDIAN_Entry', 'Key_SZ_Entry', 'Diff', 'KeyEntry', 'Key', 'Key_DWORD_BIG_ENDIAN_Entry', 'File', 'Key_BINARY_Entry', 'Key_NONE_Entry', 'Import', 'Key_DWORD_Entry', 'Key_QWORD_Entry', 'Call', 'Handle', 'Key_QWORD_LITTLE_ENDIAN_Entry', 'Socket', 'Host', 'Connection', 'Key_MULTI_SZ_Entry', 'Process', 'Key_EXPAND_SZ_Entry', 'Key_LINK_Entry', 'Directory', 'Data'}

>>> types(packages["execution"])        # Lists all Vertex classes in the "execution" package
{<class 'baguette.bakery.source.types.execution.entities.Thread'>, <class 'baguette.bakery.source.types.execution.entities.Process'>, <class 'baguette.bakery.source.types.execution.entities.Call'>}

>>> relations(packages["execution"])    # Lists all Edge classes in the "execution" package
{<class 'baguette.bakery.source.types.execution.relations.UsesAsArgument'>, <class 'baguette.bakery.source.types.execution.relations.HasChildProcess'>, <class 'baguette.bakery.source.types.execution.relations.FollowedBy'>, <class 'baguette.bakery.source.types.execution.relations.InjectedThread'>, <class 'baguette.bakery.source.types.execution.relations.HasThread'>, <class 'baguette.bakery.source.types.execution.relations.HasFirstCall'>, <class 'baguette.bakery.source.types.execution.relations.StartedThread'>, <class 'baguette.bakery.source.types.execution.relations.Runs'>, <class 'baguette.bakery.source.types.execution.relations.NextSignificantCall'>, <class 'baguette.bakery.source.types.execution.relations.StartedProcess'>}
```

All types defined in this version of BAGUETTE can be found here:

![Alt Text](https://gitlab.inria.fr/vraulin/baguette-verse/-/raw/504b13fc121c4717489b6654ab94631fdee8ec59/baguette_structure.svg "The types of vertices, edges and arrows available in BAGUETTE (most of them)")

To study a BAGUETTE sample "by hand", you can use "baguette.open" with the '.bag' file as argument or directly execute the BAGUETTE file:

```
$ ./sample.bag
BAGUETTE Interactive Prompt. Variable 'bag' holds the opened BAGUETTE file.
Most BAGUETTE packages are also loaded. Use dir() and help() to find out more.
>>> g = bag.baguette
>>> len(g.vertices)   # Number of vertices
39472

>>> len(g.edges)      # Number of edges
44410

>>> g[execution.Thread]     # All Thread vertices of this graph
IsoSet([Thread(TID = 7148, start = 1674249600.332266, stop = 1674249638.144266), Thread(TID = 7048, start = 1674249600.785266, stop = 1674249601.300266), Thread(TID = 2440, start = 1674249603.066266, stop = 1674249633.050266), [...] ])
```

You can also visualize the file using **[Gephi](https://gephi.org/)**. For that use './sample.bag --gephi'.

Note that a heterogeneous graph stores a lot of information in many different forms. For instance, each vertex/edge/arrow class can have its own attributes (for example, each 'File' vertex has a 'name' and a 'path' attribute) and these changes for each class. Use `help(cls)` to discover the available attributes and function for a given class in a Python script (for example, `help(execution.Thread)`).

## Croutons

**Croutons** is a system to extract small refined parts of BAGUETTEs. It uses **metagraphs**, which are **pattern graphs** for heterogeneous graphs, to search through datasets of BAGUETTEs for particular behaviors.

Metagraphs are stored in the metalib, and they can be created and manipulated using the interactive `metalib` prompt. For example, here is how to create your first metagraph which represent the action of writing high-entropy data into a file:
```
$ metalib
MetaLib interactive console.
Use save(MG, name) and load(name) to save and load MetaGraphs.
Use entries() to get a list of all MetaGraphs available in the library.
Use remove(name) to delete a MetaGraph from the library.
All useful types are loaded, including Graph and MetaGraph related types.
>>> entries()   # metalib is empty for now
[]

>>> MG = MetaGraph()    # Empty metagraph
>>> MG.file = MetaVertex[filesystem.File]   # First vertex
>>> MG.diff = MetaVertex[data.Diff]         # Second vertex
>>> MG.writes = MetaEdge(MG.file, MG.diff)[data.IsDiffOf]   # Edge between them
>>> MG.diff.condition = "x.written_entropy >= 6" # Condition on one vertex. Must be a string with "x" treated as a single parameter of a lambda expression

>>> save(MG, "HE-writing")  # Save metagraph
>>> entries()
['HE-writing']
```

Once you have defined the metagraphs you can export them with `metalib export` then use `toast` to search for those MetaGraph patterns in BAGUETTE graphs:

```
$ metalib export -o ./patterns.pyt
$ toast --help
usage: toast [--help] [--patterns [PATTERNS ...]] [--pool POOL] [--paint-color PAINT_COLOR | --no-paint] [--timeout TIMEOUT] [--verbosity] [--perf] baguettes [baguettes ...]

Searches for the selected patterns in BAGUETTE files.
[...]

$ toast sample.bag --patterns patterns.pyt
Toasting BAGUETTE files |████████████████████████████████████████| 1/1 [100%] in 44.8s (0.02/s)
All 1 are well-toasted!
```

You can then analyze the extracted matches in the BAGUETTE file in the "matches" attribute.

```
$ ./sample.bag
BAGUETTE Interactive Prompt. Variable 'bag' holds the opened BAGUETTE file.
Most BAGUETTE packages are also loaded. Use dir() and help() to find out more.
>>> bag.matches
<baguette.filesystem.match_file_iterator.MatchFileSequence object at 0x0000025AAFCD81A0>

>>> len(bag.matches)
23

>>> [match.graph.vertices for match in bag.matches]
[IsoSet([Process(PID = 6124, start = 1674249570.425266, stop = 1674249638.597266, [...] )])]
```

Finally, you can always use the BAGUETTE classes to expand the functionnalities of BAGUETTE. For that, you can clone the repository at https://gitlab.inria.fr/vraulin/baguette-verse. Classes, modules and packages are documented, so if you want to dig deeper, use Python's `help` function to explore the core functionnalities of BAGUETTE.