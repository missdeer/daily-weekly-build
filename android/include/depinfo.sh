#!/bin/bash -e

## Dependency versions
# Make sure to keep v_ndk and v_ndk_n in sync, the numeric version can be found in source.properties
# also remember to update path.sh

v_sdk=8512546_latest
v_ndk=r26b
v_ndk_n=26.1.10909125
v_sdk_build_tools=30.0.3

v_lua=5.2.4
v_harfbuzz=8.1.1
v_fribidi=1.0.13
v_freetype=2-13-1
v_mbedtls=2.28.4


## Dependency tree
# I would've used a dict but putting arrays in a dict is not a thing

dep_mbedtls=()
dep_dav1d=()
dep_ffmpeg=(mbedtls dav1d)
dep_freetype2=()
dep_fribidi=()
dep_harfbuzz=()
dep_libass=(freetype2 fribidi harfbuzz)
dep_lua=()
dep_libplacebo=()
dep_mpv=(ffmpeg libass lua libplacebo)
dep_mpv_android=(mpv)


## Travis-related

# pinned ffmpeg commit used by travis-ci
v_travis_ffmpeg=d5cc7acff1a4ea3e14d67faf99966c31a30d2a4d

# filename used to uniquely identify a build prefix
travis_tarball="prefix-ndk-${v_ndk}-lua-${v_lua}-harfbuzz-${v_harfbuzz}-fribidi-${v_fribidi}-freetype-${v_freetype}-mbedtls-${v_mbedtls}-ffmpeg-${v_travis_ffmpeg}.tgz"
