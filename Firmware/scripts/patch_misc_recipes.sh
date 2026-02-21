#!/bin/bash
PKGS="squeezeos-build/src/poky/meta/packages"
PKGS_SQ="squeezeos-build/src/poky/meta-squeezeos/packages"

# Patch module-init-tools
sed -i 's|http://kernel.org//pub/linux/utils/kernel/module-init-tools/module-init-tools-3.2.2.tar.bz2|file://module-init-tools-3.2.2.tar.bz2|' "$PKGS/module-init-tools/module-init-tools-cross_3.2.2.bb"

# Patch pciutils
sed -i 's|ftp://ftp.kernel.org/pub/software/utils/pciutils/pciutils-\${PV}.tar.bz2|file://pciutils-${PV}.tar.bz2|' "$PKGS/pciutils/pciutils_3.0.3.bb"

# Patch procps (in meta-squeezeos)
sed -i 's|http://procps.sourceforge.net/procps-\${PV}.tar.gz|file://procps-${PV}.tar.gz|' "$PKGS_SQ/procps/procps.inc"

echo "Recipes patched for module-init-tools, pciutils, procps."
grep "file://" "$PKGS/module-init-tools/module-init-tools-cross_3.2.2.bb"
grep "file://" "$PKGS/pciutils/pciutils_3.0.3.bb"
grep "file://" "$PKGS_SQ/procps/procps.inc"
