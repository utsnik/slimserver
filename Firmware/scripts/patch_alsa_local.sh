#!/bin/bash
RECIPE="squeezeos-build/src/poky/meta-squeezeos/packages/alsa/alsa-lib_1.0.18.bb"
sed -i 's|ftp://ftp.task.gda.pl/pub/linux/misc/alsa/lib/alsa-lib-${PV}.tar.bz2|file://alsa-lib-${PV}.tar.bz2|' "$RECIPE"
grep "SRC_URI" "$RECIPE"
