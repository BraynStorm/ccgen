import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import strictyaml as yml

from ccgen.generation import CodeGenerator
from ccgen.parser import YAMLParser


def parse(src_yml: str):
    defintion_yml = yml.load(src_yml)
    parser = YAMLParser()
    parser.visit(defintion_yml)

    codegen = CodeGenerator()
    for enum in parser.enums:
        codegen.generate_enum(enum)
    return codegen


def parse_file(src: Path, dst: Path):
    codegen = parse(src.open("r").read())
    name = str(src.stem)

    if not dst.exists():
        name = dst.stem

    with open(dst / (name + ".h"), "w") as header:
        import uuid

        u = "_header_" + str(uuid.uuid4()).replace("-", "_")
        header.write(f"#ifndef {u}\n")
        header.write(f"#define {u}\n")
        header.write("\n".join(codegen.header))
        header.write(f"\n#endif\n")

    with open(dst / (name + ".c"), "w") as source:
        source.write("\n".join(codegen.source))
    return


def main(args):
    import argparse

    p = argparse.ArgumentParser(__name__)
    p.add_argument(
        "-o",
        "--out",
        help="Destination of the output files.",
        default=".",
    )
    p.add_argument("in_yml")

    config = p.parse_args(args).__dict__
    src = Path(config["in_yml"]).absolute()
    dst = Path(config["out"]).absolute()

    parse_file(src, dst)


main(sys.argv[1:])
