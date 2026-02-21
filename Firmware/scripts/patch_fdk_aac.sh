#!/bin/bash
PKGS="squeezeos-build/src/poky/meta-squeezeos/packages/fdk-aac"

# Create files directory
mkdir -p "$PKGS/files"

# Move download (assuming in home dir based on previous curl)
mv fdk-aac-2.0.0.tar.gz "$PKGS/files/"

# Patch recipe
# Update URI to file:// and remove the git revision from the filename in the URI
sed -i 's|http://ralph.irving.sdf.org/squeezeos/${PN}-${PV}-git4edc5c4.tar.gz|file://${PN}-${PV}.tar.gz|' "$PKGS/fdk-aac_2.0.0.bb"

echo "Patched fdk-aac recipe."
grep "file://" "$PKGS/fdk-aac_2.0.0.bb"
ls -l "$PKGS/files/fdk-aac-2.0.0.tar.gz"
