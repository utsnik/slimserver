#!/bin/bash
PKGS="squeezeos-build/src/poky/meta-squeezeos/packages/alac"

# Patch recipe
# Replace the git URI with the local file URI
sed -i 's|git://github.com/macosforge/alac.git;protocol=https;branch=master|file://alac-0.1.3.tar.gz|' "$PKGS/alac_0.1.3.bb"

# Update S directory (removed git/ prefix)
sed -i 's|S="${WORKDIR}/git/codec"|S="${WORKDIR}/codec"|' "$PKGS/alac_0.1.3.bb"

echo "Patched alac recipe."
grep "file://" "$PKGS/alac_0.1.3.bb"
grep 'S="${WORKDIR}/codec"' "$PKGS/alac_0.1.3.bb"
ls -l "$PKGS/files/alac-0.1.3.tar.gz"
