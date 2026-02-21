#!/bin/bash
PKGS="squeezeos-build/src/poky/meta/packages/opkg-utils"

# Patch recipe
sed -i 's|http://downloads.slimdevices.com/poky-cache/opkg-utils_svn.openmoko.org_.trunk.src.host._4534_.tar.gz|file://opkg-utils_svn.openmoko.org_.trunk.src.host._4534_.tar.gz|' "$PKGS/opkg-utils_svn.bb"

echo "Patched opkg-utils recipe."
grep "file://" "$PKGS/opkg-utils_svn.bb"
ls -l "$PKGS/files/opkg-utils_svn.openmoko.org_.trunk.src.host._4534_.tar.gz"
