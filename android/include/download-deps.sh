#!/bin/bash -e

. ./include/depinfo.sh

[ -z "$TRAVIS" ] && TRAVIS=0
[ -z "$WGET" ] && WGET=wget

mkdir -p deps && cd deps

# mbedtls
mkdir mbedtls
cd mbedtls
$WGET https://github.com/ARMmbed/mbedtls/archive/mbedtls-$v_mbedtls.tar.gz -O - | \
	tar -xz --strip-components=1
cd ..

# dav1d
git clone --depth=1 https://code.videolan.org/videolan/dav1d.git

# ffmpeg
git clone --depth=1 https://github.com/FFmpeg/FFmpeg ffmpeg
[ $TRAVIS -eq 1 ] && ( cd ffmpeg; git checkout $v_travis_ffmpeg )

# freetype2
git clone --depth=1 git://git.sv.nongnu.org/freetype/freetype2.git -b VER-$v_freetype

# fribidi
mkdir fribidi
cd fribidi
$WGET https://github.com/fribidi/fribidi/releases/download/v$v_fribidi/fribidi-$v_fribidi.tar.xz -O - | \
	tar -xJ --strip-components=1
cd ..

# harfbuzz
mkdir harfbuzz
cd harfbuzz
$WGET https://github.com/harfbuzz/harfbuzz/releases/download/$v_harfbuzz/harfbuzz-$v_harfbuzz.tar.xz -O - | \
	tar -xJ --strip-components=1
cd ..

# libass
git clone --depth=1 https://github.com/libass/libass

# lua
mkdir lua
cd lua
$WGET http://www.lua.org/ftp/lua-$v_lua.tar.gz -O - | \
	tar -xz --strip-components=1
cd ..

# mpv (travis downloads a tar.gz snapshot instead)
[ $TRAVIS -eq 0 ] && \
	git clone --depth=1 https://github.com/mpv-player/mpv

cd ..
