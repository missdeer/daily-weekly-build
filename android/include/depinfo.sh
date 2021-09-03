#!/bin/bash -e

## Dependency versions

v_sdk=6609375_latest
v_ndk=r23
v_sdk_build_tools=29.0.2

v_lua=5.2.4
v_harfbuzz=2.9.0
v_fribidi=1.0.10
v_freetype=2-11-0
v_mbedtls=2.27.0


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
dep_mpv=(ffmpeg libass lua)
dep_mpv_android=(mpv)


## Travis-related

# pinned ffmpeg commit used by travis-ci
v_travis_ffmpeg=530ac6aa305aeda631c77f8a17e96c14c7ab1a1c

# filename used to uniquely identify a build prefix
travis_tarball="prefix-ndk-${v_ndk}-lua-${v_lua}-harfbuzz-${v_harfbuzz}-fribidi-${v_fribidi}-freetype-${v_freetype}-mbedtls-${v_mbedtls}-ffmpeg-${v_travis_ffmpeg}.tgz"
