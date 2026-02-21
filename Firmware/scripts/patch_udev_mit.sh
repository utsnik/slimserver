#!/bin/bash
MIT_RECIPE="squeezeos-build/src/poky/meta/packages/module-init-tools/module-init-tools_3.2.2.bb"

# Patch module-init-tools base recipe
sed -i 's|${KERNELORG_MIRROR}/pub/linux/utils/kernel/module-init-tools/module-init-tools-${PV}.tar.bz2|file://module-init-tools-${PV}.tar.bz2|' "$MIT_RECIPE"

echo "Patched module-init-tools base recipe."
grep "file://" "$MIT_RECIPE"

# Create udev-115 tarball
mkdir -p squeezeos-build/src/poky/sources/git/udev
cd squeezeos-build/src/poky/sources/git/udev
git clone --depth 1 -b 115 https://git.kernel.org/pub/scm/linux/hotplug/udev.git .
# Verify we are on the right version
git describe --tags

# Create tarball (prefix string is udev-115/)
# Note: we need to make sure the structure matches what bitbake expects (usually a folder named udev-115)
mkdir -p ../udev-115
cp -r * ../udev-115/
cd ..
tar -czf udev-115.tar.gz udev-115/
rm -rf udev udev-115

# Move to a place where we can link it (we will need to find the udev recipe path later, 
# for now let's put it in sources since we can use file:// override or PREMIRROR)
# Actually, let's put it in the pciutils/module-init-tools location for consistency or 
# verify where the udev recipe lives first.
# putting it in sources root for now.
mv udev-115.tar.gz ../../
