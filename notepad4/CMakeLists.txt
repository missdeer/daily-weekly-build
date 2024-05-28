cmake_minimum_required(VERSION 3.5)

project(notepad4 VERSION 0.1)
    
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

option(NOAVX2 "Target CPU does NOT support AVX2")

if(NOT NOAVX2 AND NOT CMAKE_BUILD_TYPE MATCHES Debug)
    if(CMAKE_SYSTEM_PROCESSOR STREQUAL "AMD64" OR CMAKE_SYSTEM_PROCESSOR STREQUAL "amd64" OR CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
        if( ${CMAKE_CXX_COMPILER_ID} STREQUAL "IntelLLVM")
            add_compile_options("/QxCORE-AVX2" "-O3" "-mavx2")
        elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC" OR "${CMAKE_CXX_SIMULATE_ID}" STREQUAL "MSVC")
            add_compile_options("/Ot" "/fp:fast" "/Gv" "/O2" "/arch:AVX2")
        else()
            add_compile_options("-mavx2" "-mpopcnt" "-mbmi" "-mbmi2" "-mlzcnt" "-mmovbe")
        endif()
    endif()
endif()
if(MINGW)
  add_link_options("-municode")
endif()

add_compile_definitions(
    _WIN64
    _WIN32_WINNT=0x0601 
    WINVER=0x0601 
    _WINDOWS
    NOMINMAX
    WIN32_LEAN_AND_MEAN
    STRICT_TYPED_ITEMIDS
    NO_CXX11_REGEX
    UNICODE
    _UNICODE
    _CRT_SECURE_NO_WARNINGS
    _SCL_SECURE_NO_WARNINGS
)
include_directories(scintilla/include scintilla/lexlib scintilla/src scintilla/win32 src src/EditLexers)
				 
find_package(OpenMP REQUIRED)
file(GLOB
        EditLexers
        src/EditLexers/*.cpp
        )

file(GLOB
        src
        src/*.c
        src/*.cpp
        )

file(GLOB
        lexlib
        scintilla/lexlib/*.cxx
        )

file(GLOB
        lexers
        scintilla/lexers/*.cxx
        )

file(GLOB
        scintilla
        scintilla/src/*.cxx
        )

file(GLOB
        win32
        scintilla/win32/*.cxx
        )

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC" OR "${CMAKE_CXX_SIMULATE_ID}" STREQUAL "MSVC")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /MANIFEST:NO")
endif()
add_executable(${PROJECT_NAME} ${EditLexers} ${src} ${lexlib} ${lexers} ${scintilla} ${win32} src/Notepad4.rc)
target_link_libraries(${PROJECT_NAME} PRIVATE comctl32 shlwapi imm32 uxtheme OpenMP::OpenMP_CXX)
set_target_properties(${PROJECT_NAME} PROPERTIES WIN32_EXECUTABLE ON)

file(GLOB
        matepath_src
        matepath/src/*.c
        matepath/src/*.cpp
        )
add_executable(matepath ${matepath_src} matepath/src/matepath.rc)
target_link_libraries(matepath PRIVATE comctl32 shlwapi uxtheme)
set_target_properties(matepath PROPERTIES WIN32_EXECUTABLE ON)
