# Auxiliary file for CCGEN in Cmake
# 
# Provides a ccgen(...) function to compile all *.ccgen.yaml files to a .c/.h pair
# Usage: after you define your target do:
#   include(ccgen.cmake)
#   ...
#   add_executable(MY_TARGET src1.c, src2.c, src3.yaml)
#   ...
#   ccgen(MY_TARGET)
#   target
#
# To use, feel free to copy this file to your CMakeLists.txt directory.

function(ccgen target)
    get_target_property(sources ${target} SOURCES)
    foreach(yaml_file in ${sources})
        cmake_path(GET yaml_file EXTENSION ext)
        if("${ext}" MATCHES ".*\.ccgen\.yaml$")
            cmake_path(GET yaml_file STEM gen)
            add_custom_command(
                COMMAND ${Python3_EXECUTABLE} -m ccgen "${yaml_file}" -o "${CMAKE_BINARY_DIR}"
                OUTPUT
                    "${CMAKE_BINARY_DIR}/${gen}.ccgen.c"
                    "${CMAKE_BINARY_DIR}/${gen}.ccgen.h"
                DEPENDS
                    "${yaml_file}"
                COMMENT "CCGen - genetate files."
                WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
            )
            target_sources(
                ${target}
                PRIVATE
                "${CMAKE_BINARY_DIR}/${gen}.ccgen.c"
                "${CMAKE_BINARY_DIR}/${gen}.ccgen.h"
            )
        endif()
    endforeach()
    target_include_directories(${target} PUBLIC "${CMAKE_BINARY_DIR}")
endfunction()
