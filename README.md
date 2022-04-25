# CCGen
C code generator, using YAML input.

Generates enums from YAML specification.

Requires Python 3.10

## Features
TODO

## Installation
```
pip install -U git+https://github.com/BraynStorm/ccgen
```

## Usage
Use the following snippet in your top-level CMakeLists.txt
```cmake
find_package(Python3 REQUIRED COMPONENTS Interpreter)
execute_process(COMMAND ${Python3_EXECUTABLE} -m ccgen.cmake OUTPUT_VARIABLE CCGEN_CMAKE OUTPUT_STRIP_TRAILING_WHITESPACE)
list(APPEND CMAKE_MODULE_PATH "${CCGEN_CMAKE}")
include(ccgen)
```
## Example CMake project
See the examples/ folder for full examples.

### Structure
```
myproject
|   CMakeLists.txt
|   enums.ccgen.yaml
|   main.c
```

### enums.ccgen.yaml
```yaml
enums:
    MyEnum:
        attributes:
            - to_string
        items:
            - Alpha
            - Beta
            - Gamma
```

### CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.23)

project(MyProject)

find_package(Python3 REQUIRED COMPONENTS Interpreter)
execute_process(COMMAND ${Python3_EXECUTABLE} -m ccgen.cmake OUTPUT_VARIABLE CCGEN_CMAKE OUTPUT_STRIP_TRAILING_WHITESPACE)
list(APPEND CMAKE_MODULE_PATH "${CCGEN_CMAKE}")
include(ccgen)

# Important: Name your YAML files *.ccgen.yaml
add_executable(my_exec main.c enums.ccgen.yaml)
ccgen(my_exec)
```

### main.c
```c
#include <stdio.h>

#include "enums.ccgen.h"

int main(int argc, char* argv[])
{
    puts(MyEnum_GetName(MyEnum_Alpha));
    return 0;
}
```

### Output
```
Alpha

```

## Examples
### Input
```yaml
enums:
  ItemType:
    attributes:
      - bits
    items:
      - Quest
      - Equippable
      - Consumable

  ItemSlot:
    attributes:
      - to_string
    items:
      - Head
      - Neck
      - Shoulder
      - Back
      - Trinket
      - Shirt
      - Tabard
      - Chest
      - Hand
      - Finger
      - Leg
      - Waist
      - Wrist
      - Weapon
```

### Command
```
python -m ccgen [-o OUTPUT_DIR] INPUT_YAML 
```
### Output (header)
```c
#ifndef _header_82140b6b_0ebe_478e_af5d_4631101893dc
#define _header_82140b6b_0ebe_478e_af5d_4631101893dc
enum ItemType
{
    ItemType_Quest = 1,
    ItemType_Equippable = 2,
    ItemType_Consumable = 4,
};

enum ItemSlot
{
    ItemSlot_Head = 0,
    ItemSlot_Neck = 1,
    ItemSlot_Shoulder = 2,
    ItemSlot_Back = 3,
    ItemSlot_Trinket = 4,
    ItemSlot_Shirt = 5,
    ItemSlot_Tabard = 6,
    ItemSlot_Chest = 7,
    ItemSlot_Hand = 8,
    ItemSlot_Finger = 9,
    ItemSlot_Leg = 10,
    ItemSlot_Waist = 11,
    ItemSlot_Wrist = 12,
    ItemSlot_Weapon = 13,
};

char const* ItemSlot_GetName(enum ItemSlot e);
#endif

```

### Output (source)
```c
static char const* ItemSlot_names[] = {
    "Head",
    "Neck",
    "Shoulder",
    "Back",
    "Trinket",
    "Shirt",
    "Tabard",
    "Chest",
    "Hand",
    "Finger",
    "Leg",
    "Waist",
    "Wrist",
    "Weapon",
};

char const* ItemSlot_GetName(enum ItemSlot e)
{
    return ItemSlot_names[e];
}
```

