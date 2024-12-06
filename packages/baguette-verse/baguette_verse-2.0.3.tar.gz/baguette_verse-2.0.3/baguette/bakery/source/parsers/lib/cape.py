"""
This is the ParserClass for Cape V2 reports.
"""

import ast
from pathlib import Path, PurePath
from types import NotImplementedType
from typing import Any, Iterable, Iterator, Literal, TypedDict, NotRequired
from .....filesystem.binary_decoder import CodecStream
from ..abc import CallInfo, MachineInfo, AbstractParser, ProcessInfo, ThreadInfo
from datetime import datetime 



class Environ(TypedDict):

    UserName : str
    ComputerName : str
    WindowsPath : str
    TempPath : str
    CommandLine : str
    RegisteredOwner : str
    RegisteredOrganization : str
    ProductName : str
    SystemVolumeSerialNumber : str
    SystemVolumeGUID : str
    MachineGUID : str

class ProcessTree(TypedDict):

    name : str
    pid : int
    parent_id : int
    module_path : str
    children : "list[ProcessTree]"
    threads : list[int]
    environ : Environ
    #first_seen: str

class Summary(TypedDict):

    files: list[str]
    read_files: list[str]
    write_files: list[str]
    delete_files: list[str]
    keys: list[str]
    read_keys: list[str]
    write_keys: list[str]
    delete_keys: list[str]
    executed_commands: list[str]
    resolved_apis: list[str]
    mutexes: list[str]
    created_services: list[str]
    started_services: list[str]




class ArgumentInfo(TypedDict):

    name : str
    value : str
    pretty_value : NotRequired[str]

RawCallInfo = TypedDict("RawCallInfo", {
    "timestamp" : str,
    "thread_id" : str,
    "caller" : str,
    "parentcaller" : str,
    "category" : str,
    "api" : str,
    "status" : bool,
    "return" : str,
    "arguments" : list[ArgumentInfo],
    "repeated" : int,
    "id" : int
})

class RawProcessInfo(TypedDict):

    process_id : int
    process_name : str
    parent_id : int
    module_path : str
    first_seen : str
    calls : list[RawCallInfo]
    threads : list[int]
    environ : Environ
    #process_path : str



class CapeParser(AbstractParser):

    """
    A report parser specialized for the Cape V2 sandbox.
    """

    report_name = "cape"

    from json import load, JSONDecodeError as __JSONDecodeError
    from ..abc import ProcessInfo as __ProcessInfo, ImportInfo as __ImportInfo, ThreadInfo as __ThreadInfo, CallInfo as __CallInfo
    from ..utils import MissingBehavioralInfoError as __MissingBehavioralInfoError, MissingSamplePathError as __MissingSamplePathError
    from ...utils import path_factory
    __path_factory = staticmethod(path_factory)
    __load = staticmethod(load)
    del load, path_factory

    def __init__(self, p: CodecStream) -> None:
        super().__init__(p)
        self.__path = p
        self.__execution_tree : "list[tuple[ProcessInfo | None, ProcessInfo]]" = []
        self.__machines : "tuple[MachineInfo, ...] | None" = None
        self.__host : "MachineInfo | None" = None
        with p.open("r") as f:
            self.__data = CapeParser.__load(f)
        
    @staticmethod
    def match_report_type(p: CodecStream) -> bool | NotImplementedType:
        with p.open("r") as f:
            try:
                data = CapeParser.__load(f)
            except CapeParser.__JSONDecodeError:
                return False
        #return isinstance(data, dict) and "debug" in data and isinstance(data["debug"], dict) and "CAPE" in data
        #problem1: to check ! 
        return isinstance(data,dict) and 'info' in data and isinstance(data['info'],dict) and 'version' in data['info'] and isinstance(data['info']['version'],str) and "CAPE" in data['info']['version']
    
    def process_tree_iterator(self) -> Iterator[tuple[ProcessInfo | None, ProcessInfo]]:
        if "behavior" not in self.__data:
            raise CapeParser.__MissingBehavioralInfoError(f"Given Cape report does not contain any behavioral info")
        from Viper.frozendict import frozendict
        from ...utils import parse_command_line
        from .....logger import logger
        strTimeformat = "%Y-%m-%d %H:%M:%S,%f"
        def clean_dict(d : "dict[str, Any]"):
            cd = {}
            for k, v in d.items():
                if isinstance(v, list):
                    cd[k] = tuple(v)
                elif isinstance(v, dict):
                    cd[k] = frozendict(v)
                else:
                    cd[k] = v
            return cd
        
        def has_arg(c : RawCallInfo, arg : str) -> bool:
            for d in c["arguments"]:
                if d["name"] == arg:
                    return True
            
            return False


        def get_arg(c : RawCallInfo, arg : str) -> str:
            for d in c["arguments"]:
                if d["name"] == arg:
                    return d["value"]
            raise KeyError(f"No such argument : '{arg}'")
        
        def set_arg(c : RawCallInfo, arg : str, value : str, pretty_value: str | None = None):
            for d in c["arguments"]:
                if d["name"] == arg:
                    d["value"] = value
                    if pretty_value is not None:
                        d['pretty_value'] = pretty_value
                    return
            c["arguments"].append({
                 "name" : arg,
                "value" : value
            } | ({"pretty_value": pretty_value} if pretty_value is not None else {})) # type: ignore

        def handle_tracker(it : "Iterable[RawCallInfo]") -> "Iterable[RawCallInfo]":
            handles_positions : dict[int, int] = {}
            
            for c in it:
                match c["api"]:
                    case "NtCreateFile" | "NtOpenFile":
                        handles_positions[int(get_arg(c, "FileHandle"), base=16)] = 0
                    case "NtReadFile" | "NtWriteFile":
                        h = int(get_arg(c, "FileHandle"), base=16)
                        if h not in handles_positions:
                            logger.warning(f"Got an IO operation on an unknown handle: {hex(h)} in call #{c['id']}")
                        set_arg(c, "Offset", hex(handles_positions.setdefault(h, 0)))
                        handles_positions[h] += int(get_arg(c, "Length"))
                    case "NtClose":
                        if (h := int(get_arg(c, "Handle"), base=16)) in handles_positions:
                            handles_positions.pop(h)
                yield c
        
        def handle_regtype_tracker(it : "Iterable[RawCallInfo]") -> "Iterable[RawCallInfo]":
            for c in it:
                match c["api"]:
                    case 'NtQueryValueKey' | 'RegQueryValueExW' | 'RegQueryValueExA' | "RegEnumValueW" | 'RegEnumValueA' | 'NtEnumerateValueKey':
                        if not has_arg(c, "Data"):
                            set_arg(c,"Type","0","REG_NONE") 
                            set_arg(c,"Data","")
                            
                        if not has_arg(c,"Type"):
                            set_arg(c,"Type","1","REG_SZ")
                    

                yield c


        def thread_info_iterator(p : "RawProcessInfo", ident : int):
        #def thread_info_iterator(p : "processes"):
        ### to check!
            starts : "dict[int, float]" = {}
            stops : "dict[int, float]" = {}
            calls : "dict[int, list[CallInfo]]" = {}
            
            for i, c in enumerate(handle_regtype_tracker(handle_tracker(p["calls"]))):
                starts.setdefault(int(c["thread_id"]), datetime.strptime(c["timestamp"],strTimeformat).timestamp())
                stops[int(c["thread_id"])] = datetime.strptime(c["timestamp"],strTimeformat).timestamp()
                calls.setdefault(int(c["thread_id"]), []).append(self.translator.translate(CapeParser.__CallInfo(c["api"], bool(c["status"]), int(c["return"],base=16), clean_dict({arg['name']: arg['value'] for arg in c["arguments"]}), clean_dict({arg['name']: arg['pretty_value'] for arg in c["arguments"] if 'pretty_value' in arg}), datetime.strptime(c["timestamp"],strTimeformat).timestamp(), (ident, i))))
            return tuple(ThreadInfo(TID, starts[TID], stops[TID], tuple(calls[TID])) for TID in starts)
        
        def explore_process_tree(p : "ProcessTree", parent : "ProcessInfo | None" = None) -> "Iterator[tuple[ProcessInfo | None, ProcessInfo]]":
            data : "RawProcessInfo"
            raw_process_info = None
            ident = None
            for i, data in enumerate(self.__data["behavior"]["processes"]):
                if data["process_id"] == p["pid"] and data["parent_id"] == p["parent_id"]:
                    raw_process_info = data
                    ident = i
                    break
            if raw_process_info is None or ident is None:
                return
            threads = thread_info_iterator(raw_process_info, ident)
            process_info = CapeParser.__ProcessInfo(
                p["pid"],
                datetime.strptime(data["first_seen"],strTimeformat).timestamp(),
                max((t.stop for t in threads), default=float("inf")),
                threads,
                tuple(parse_command_line(p["environ"]["CommandLine"],executable=raw_process_info["module_path"])), 
                CapeParser.__path_factory(raw_process_info["module_path"]), 
                ### Problem 4: I didn't find imgsize or filepath in the cape report.
                #tuple(CapeParser.__ImportInfo(CapeParser.__path_factory(i["filepath"]), i["imgsize"]) for i in raw_process_info["module_path"])          
                ()
            )

            yield (parent, process_info)
            for pi in p["children"]:
                yield from explore_process_tree(pi, process_info)

        if not self.__execution_tree:
            process_tree : "list[ProcessTree]" = self.__data["behavior"]["processtree"].copy()
            self.__execution_tree.extend((p1, p2) for p in process_tree for p1, p2 in explore_process_tree(p))
        
        yield from self.__execution_tree

    def machines(self) -> Iterable[MachineInfo]:
        if self.__machines is not None:
            return self.__machines
        hosts : set[str] = set()
        if "hosts" in self.__data["network"] and isinstance(self.__data["network"]["hosts"], list):
            hosts = set(h["ip"] for h in self.__data["network"]["hosts"])
        domains : dict[str, str] = {data["ip"] : data["domain"] for data in self.__data["network"].get("domains", [])}
        hosts.difference_update(domains)
        machines = []
        for add, domain in domains.items():
            machines.append(MachineInfo(add, "", domain))
        machines.extend(MachineInfo(add, "", "") for add in hosts)
        self.__machines = tuple(machines)
        return self.__machines
    
    def host(self) -> MachineInfo:
        if self.__host is not None:
            return self.__host
        host_ip = ""
        if "dns_servers" in self.__data["network"] and "udp" in self.__data["network"]:
            for dns_ip in self.__data["network"]["dns"]:### Problem 5: no dns_servers 
                for data in self.__data["network"]["udp"]:
                    if data["dst"] == dns_ip:
                        host_ip = data["src"]
                        break
                if host_ip:
                    break
        host_ip = host_ip or "127.0.0.1"
        domain = "localhost" if host_ip == "127.0.0.1" else ""
        hostname = ""
        for parent, p in self.process_tree_iterator():
            for t in p.threads:
                for api in t.calls:
                    if api.API in ("GetComputerNameW", "GetComputerNameA") and (name := api.arguments["computer_name"]):
                        hostname = name
                        break
                if hostname:
                    break
            if hostname:
                    break
        else:
            hostname = "host"
        self.__host = MachineInfo(host_ip, hostname, domain)
        return self.__host

    def sample_file_path(self) -> PurePath:
        import re
        from ...utils import path_factory
        ### design new expressions ! 
        #expr1 = re.compile(r"^\d*-\d*-\d* \d*:\d*:\d*,\d* \[lib\.api\.process\] INFO: Successfully executed process from path (.+?) with arguments (.+) and pid \d+\n$")
        #expr2 = re.compile(r"^\d*-\d*-\d* \d*:\d*:\d*,\d* \[lib\.api\.process\] ERROR: Failed to execute process from path (.+?) with arguments (.+) \(Error: Command (.+) returned non-zero exit status \d+\)\n$")
        expr1 = re.compile(r"^\d*-\d*-\d* \d*:\d*:\d*,\d* \[lib\.api\.process\] INFO: Successfully executed process from path \"(.+?)\" with arguments (.+) with pid \d+$")
        expr2 = re.compile(r"^\d*-\d*-\d* \d*:\d*:\d*,\d* \[lib\.api\.process\] ERROR: Failed to execute process from path \"(.+?)\" with arguments (.+) \(Error: Command (.+) returned non-zero exit status \d+\)$")

        line : str
        log = ast.literal_eval(f"{repr(self.__data['debug']['log'])}")
        for line in log.splitlines():
            if match := expr1.fullmatch(line):
                command_line : list[str] = [eval(repr(match.group(1)))] + (eval(match.group(2)) or [])
                break
            if match := expr2.fullmatch(line):
                command_line : list[str] = [eval(repr(match.group(1)))] + (eval(match.group(2)) or [])
                break
        else:
            raise CapeParser.__MissingSamplePathError(f"Could not find the log that signals the execution of the sample process in sample")
        file_name : str = self.__data["target"]["file"]["name"]
        expr3 = re.compile(r"^(.*),.*?$")       # Sometimes, its in the form <path,something else>
        for param in command_line:
            try:
                p = path_factory(param)
                if p.name == file_name or p.stem == file_name:
                    return p
                if (match := expr3.fullmatch(param)):
                    p = path_factory(match.group(1))
                    if p.name == file_name or p.stem == file_name:      # p.stem because an extension might have been added
                        return p
            except:
                pass
        raise CapeParser.__MissingSamplePathError(f"Could not find the sample file path in the sample process command line in sample")
    
    def platform(self) -> Literal['Windows', 'Unix']:
        ### Problem 6 : Where is the declaration of Literal ? 
        ### No platform attribute is found. 
        #return self.__data["info"]["platform"].title()
        if 'C:\\Windows' in self.__data['debug']["log"]:
            return 'Windows'
        else:
            return 'Unix'
        
