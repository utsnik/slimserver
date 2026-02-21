#!/bin/bash
RECIPE="squeezeos-build/src/poky/meta-squeezeos/packages/meta/external-csl-toolchain_2010q1-202.bb"
sed -i 's|http://www.codesourcery.com/public/gnu_toolchain/arm-none-linux-gnueabi/arm-${PV}-arm-none-linux-gnueabi-i686-pc-linux-gnu.tar.bz2|file://arm-2010q1-202-arm-none-linux-gnueabi-i686-pc-linux-gnu.tar.bz2|' "$RECIPE"
grep "SRC_URI" "$RECIPE"
