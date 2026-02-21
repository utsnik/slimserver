#!/bin/bash
RECIPE="squeezeos-build/src/poky/meta/packages/file/file_4.18.bb"
sed -i 's|ftp://ftp.astron.com/pub/file/file-\${PV}.tar.gz|file://file-${PV}.tar.gz|' "$RECIPE"
grep "SRC_URI" "$RECIPE"
