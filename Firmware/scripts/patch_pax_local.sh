#!/bin/bash
RECIPE="squeezeos-build/src/poky/meta/packages/pax-utils/pax-utils_0.1.19.bb"
sed -i 's|SRC_URI     = "\${GENTOO_MIRROR}/pax-utils-\${PV}.tar.bz2"|SRC_URI     = "file://pax-utils-${PV}.tar.bz2"|' "$RECIPE"
grep "SRC_URI" "$RECIPE"
