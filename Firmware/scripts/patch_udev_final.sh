#!/bin/bash
PKGS="squeezeos-build/src/poky/meta/packages"
PKGS_SQ="squeezeos-build/src/poky/meta-squeezeos/packages"

# Create files directory for udev
mkdir -p "$PKGS/udev/files"

# Move the manually created tarball to the files directory
# Assumes the previous script left udev-115.tar.gz in the root of sources or we can find it
# Based on previous step, it was moved to ../.. from udev dir, which is sources root
mv squeezeos-build/src/poky/sources/udev-115.tar.gz "$PKGS/udev/files/"

# Patch meta udev recipe
sed -i 's|http://kernel.org/pub/linux/utils/kernel/hotplug/udev-${PV}.tar.gz|file://udev-${PV}.tar.gz|' "$PKGS/udev/udev_115.bb"

# Patch meta-squeezeos udev recipe (if it defines SRC_URI)
sed -i 's|http://kernel.org/pub/linux/utils/kernel/hotplug/udev-${PV}.tar.gz|file://udev-${PV}.tar.gz|' "$PKGS_SQ/udev/udev_115.bb"

echo "Patched udev recipes and moved tarball."
ls -l "$PKGS/udev/files/udev-115.tar.gz"
grep "file://" "$PKGS/udev/udev_115.bb"
grep "file://" "$PKGS_SQ/udev/udev_115.bb"
