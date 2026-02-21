#!/bin/bash
RECIPE="squeezeos-build/src/poky/meta/packages/zlib/zlib_1.2.3.bb"
sed -i 's|SRC_URI = ".*zlib-1.2.3.tar.bz2|SRC_URI = "https://web.archive.org/web/20120531173611id_/http://www.zlib.net/zlib-1.2.3.tar.bz2|' "$RECIPE"
grep "SRC_URI" "$RECIPE"
