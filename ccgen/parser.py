from dataclasses import dataclass, field
import enum
from sys import stderr
from typing import Iterable, List

from strictyaml import YAML

from ccgen.types import *


@dataclass
class YAMLParser:
    enums: List[Enum] = field(default_factory=list)

    def current_enum(self) -> Enum:
        return self.enums[-1]

    def visit_enums(self, node: YAML):
        for enum_name, enum_def in node.items():
            e = Enum(str(enum_name), {})
            self.enums.append(e)

            if 'attributes' in enum_def:
                attributes = self.visit_attributes(enum_def["attributes"])
                for attr in attributes:
                    f = getattr(self, f"process_enum_attribute_{attr}")
                    f(e)

            if enum_def.is_sequence():
                yaml_items = enum_def
            elif 'items' in enum_def:
                yaml_items = enum_def["items"]
            else:
                print("Enums without items/values are not permitted.")

            items = self.visit_items(yaml_items, e)
            e.items = items

    def process_enum_attribute_bits(self, enum: Enum):
        enum.is_bits = True

    def process_enum_attribute_to_string(self, enum: Enum):
        enum.is_stringable = True

    def visit_attributes(self, node: YAML) -> Iterable[str]:
        return map(str, node)

    def visit_items(self, node: YAML, e: Enum) -> Dict[str, Optional[int]]:
        items: Dict[str, Optional[int]] = dict()
        if node.is_sequence():
            if e.is_bits:
                for i, item in enumerate(node):
                    items[str(item)] = 1 << i
            else:
                for i, item in enumerate(node):
                    items[str(item)] = i
        elif node.is_mapping():
            # TODO: implement
            raise NotImplementedError()
        return items

    def visit_structs(self, node: YAML):
        # TODO(bozho2):
        #   Implement struct generation
        raise NotImplementedError()

    def visit(self, node: YAML) -> "YAMLParser":
        for section_name, section_node in node.items():
            visitor = getattr(self, f"visit_{section_name}")
            visitor(section_node)
        return self
