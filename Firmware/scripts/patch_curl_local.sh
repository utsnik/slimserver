#!/bin/bash
RECIPE="squeezeos-build/src/poky/meta/packages/curl/curl_7.18.0.bb"
sed -i 's|SRC_URI = "http://curl.haxx.se/download/curl-${PV}.tar.bz2|SRC_URI = "file://curl-${PV}.tar.bz2|' "$RECIPE"
grep "SRC_URI" "$RECIPE"
