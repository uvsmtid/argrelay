from dataclasses import dataclass

from argrelay.enum_desc.ArgSource import ArgSource


# TODO: Forget about coords everywhere, use args for input, maybe coord for the term of core library.
@dataclass
class ArgValue:
    arg_value: str
    arg_source: ArgSource