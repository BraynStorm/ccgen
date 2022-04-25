cmake_minimum_required(VERSION 3.23)
project(MyProject)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

execute_process(COMMAND ${Python3_EXECUTABLE} -m ccgen.cmake OUTPUT_VARIABLE CCGEN_CMAKE OUTPUT_STRIP_TRAILING_WHITESPACE)
list(APPEND CMAKE_MODULE_PATH "${CCGEN_CMAKE}")

include(ccgen)

add_executable(MyExec main.c enums.ccgen.yaml)
ccgen(MyExec)
