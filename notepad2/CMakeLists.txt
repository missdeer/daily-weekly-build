cmake_minimum_required(VERSION 3.5)

project(notepad2 VERSION 0.1)
    
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

if( ${CMAKE_CXX_COMPILER_ID} STREQUAL "IntelLLVM")
    add_compile_options("/QxCORE-AVX2" "-O3" "-mavx2")
elseif (${CMAKE_CXX_COMPILER_ID} STREQUAL "Clang")
    add_compile_options("-mavx2" "-mpopcnt" "-mbmi" "-mbmi2" "-mlzcnt" "-mmovbe")
elseif (${CMAKE_CXX_COMPILER_ID} STREQUAL "GNU")
    add_compile_options("-mavx2" "-mpopcnt" "-mbmi" "-mbmi2" "-mlzcnt" "-mmovbe")
else()
    add_compile_options("/Ot" "/fp:fast" "/Gv" "/arch:AVX2")
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

file(GLOB
        EditLexers
        src/EditLexers/*.c
        )

file(GLOB
        src
        src/*.c*
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

set (CMAKE_EXE_LINKER_FLAGS /MANIFEST:NO )
add_executable(${PROJECT_NAME} ${EditLexers} ${src} ${lexlib} ${lexers} ${scintilla} ${win32} src/Notepad2.rc)
target_link_libraries(${PROJECT_NAME} PRIVATE comctl32 shlwapi imm32 uxtheme)
set_target_properties(${PROJECT_NAME} PROPERTIES WIN32_EXECUTABLE ON)