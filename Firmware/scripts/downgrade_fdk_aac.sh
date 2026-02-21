#!/bin/bash
PKGS="squeezeos-build/src/poky/meta-squeezeos/packages/fdk-aac"

# Remove old tarball and move new one
rm -f "$PKGS/files/fdk-aac-2.0.0.tar.gz"
mv fdk-aac-0.1.6.tar.gz "$PKGS/files/"

# Rename and patch recipe
mv "$PKGS/fdk-aac_2.0.0.bb" "$PKGS/fdk-aac_0.1.6.bb"
sed -i 's|PN}-${PV}.tar.gz|PN}-${PV}.tar.gz|' "$PKGS/fdk-aac_0.1.6.bb"

echo "Downgraded fdk-aac recipe to 0.1.6."
ls -l "$PKGS/files/fdk-aac-0.1.6.tar.gz"
ls -l "$PKGS/fdk-aac_0.1.6.bb"
