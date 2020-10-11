#!/bin/bash -e

# Change to preferred versions
MPV_VERSION="0.32.0"
FFMPEG_VERSION="4.3.1"
LIBASS_VERSION="0.14.0"
FREETYPE_VERSION="2.10.2"
HARFBUZZ_VERSION="2.6.7"
FRIBIDI_VERSION="1.0.10"
UCHARDET_VERSION="0.0.7"

rm -rf src
mkdir src
[ -d "downloads" ] || mkdir downloads;

MPV_URL="https://github.com/mpv-player/mpv/archive/master.tar.gz"
curl -f -L $MPV_URL -o downloads/mpv.tar.gz
tar xvf downloads/mpv.tar.gz -C src

FFMPEG_URL="http://www.ffmpeg.org/releases/ffmpeg-$FFMPEG_VERSION.tar.xz"
curl -f -L $FFMPEG_URL -o downloads/FFmpeg.tar.xz
tar xvf downloads/FFmpeg.tar.xz -C src

LIBASS_URL="https://github.com/libass/libass/archive/master.tar.gz"
FRIBIDI_URL="https://github.com/fribidi/fribidi/releases/download/v$FRIBIDI_VERSION/fribidi-$FRIBIDI_VERSION.tar.xz"
FREETYPE_URL="https://sourceforge.net/projects/freetype/files/freetype2/$FREETYPE_VERSION/freetype-$FREETYPE_VERSION.tar.xz"
HARFBUZZ_URL="https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-$HARFBUZZ_VERSION.tar.xz"
UCHARDET_URL="https://www.freedesktop.org/software/uchardet/releases/uchardet-$UCHARDET_VERSION.tar.xz"

for URL in $UCHARDET_URL $FREETYPE_URL $HARFBUZZ_URL $FRIBIDI_URL $LIBASS_URL; do
	TARNAME=${URL##*/}
    if [ ! -f "downloads/$TARNAME" ]; then
	    curl -f -L $URL -o downloads/$TARNAME
    fi
    echo "$TARNAME"
    tar xvf downloads/$TARNAME -C src
done

echo "\033[1;32mDownloaded: \033[0m\n mpv: $MPV_VERSION \
                            \n FFmpeg: $FFMPEG_VERSION \
                            \n libass: $LIBASS_VERSION \
                            \n freetype: $FREETYPE_VERSION \
                            \n harfbuzz: $HARFBUZZ_VERSION \
                            \n fribidi: $FRIBIDI_VERSION \
                            \n uchardet: $UCHARDET_VERSION "
