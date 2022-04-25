cmake_minimum_required(VERSION 3.23)
project(MyProject)

include(ccgen.cmake)

add_executable(MyExec main.c enums.ccgen.yaml)

ccgen(MyExec)
