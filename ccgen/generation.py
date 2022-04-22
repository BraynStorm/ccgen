from dataclasses import dataclass, field
from typing import List

from ccgen.types import Enum


@dataclass
class CodeGenerator:
    header: List[str] = field(default_factory=list)
    source: List[str] = field(default_factory=list)

    def generate_enum(self, enum: Enum):
        e = f"enum {enum.name}\n{{\n"
        for name, value in enum.items.items():
            e += f"    {enum.name}_{name} = {value},\n"
        e += "};\n"
        self.header.append(e)

        if enum.is_stringable:
            if enum.is_bits:
                # TODO(bozho2):
                #   Implement bit stringify
                raise NotImplementedError()
            array_name = f"{enum.name}_names"
            decl = f"char const* {enum.name}_GetName(enum {enum.name} e)"
            arr = f"static char const* {array_name}[] = {{\n"
            for name, value in enum.items.items():
                arr += f'    "{name}",\n'
            arr += "};\n"
            self.header.append(f"{decl};")
            self.source.append(arr)
            self.source.append(f"{decl}\n{{\n    return {array_name}[e];\n}}")
