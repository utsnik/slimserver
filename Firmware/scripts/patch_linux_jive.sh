#!/bin/bash
PKGS="squeezeos-build/src/poky/meta-squeezeos/packages/linux"

# Patch recipe
# Replace the SVN URI with the local file URI for the s3c2412 module
sed -i 's|${SQUEEZEOS_SVN};module=s3c2412|file://s3c2412.tar.gz|' "$PKGS/linux-jive_svn.bb"

echo "Patched linux-jive recipe."
grep "file://" "$PKGS/linux-jive_svn.bb"
ls -l "$PKGS/files/s3c2412.tar.gz"
