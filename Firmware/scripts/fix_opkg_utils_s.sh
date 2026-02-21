#!/bin/bash
PKGS="squeezeos-build/src/poky/meta/packages/opkg-utils"

# Patch recipe to set S to WORKDIR
sed -i 's|S = "${WORKDIR}/opkg-utils"|S = "${WORKDIR}"|g' "$PKGS/opkg-utils_svn.bb"

echo "Updated S in opkg-utils recipe."
grep "S =" "$PKGS/opkg-utils_svn.bb"
