#!/bin/bash
RECIPE_NATIVE="squeezeos-build/src/poky/meta-squeezeos/packages/git/git-native_1.5.2.3.bb"
RECIPE_TARGET="squeezeos-build/src/poky/meta-squeezeos/packages/git/git_1.5.2.3.bb"
RECIPE_INC="squeezeos-build/src/poky/meta-squeezeos/packages/git/git.inc"

# Patch all of them just in case, though usually only one defines SRC_URI efficiently
sed -i 's|http://www.kernel.org/pub/software/scm/git/git-${PV}.tar.bz2|file://git-${PV}.tar.bz2|' "$RECIPE_NATIVE"
sed -i 's|http://www.kernel.org/pub/software/scm/git/git-${PV}.tar.bz2|file://git-${PV}.tar.bz2|' "$RECIPE_TARGET"
sed -i 's|http://www.kernel.org/pub/software/scm/git/git-${PV}.tar.bz2|file://git-${PV}.tar.bz2|' "$RECIPE_INC"

echo "Checking Native:"
grep "SRC_URI" "$RECIPE_NATIVE"
echo "Checking Target:"
grep "SRC_URI" "$RECIPE_TARGET"
echo "Checking Inc:"
grep "SRC_URI" "$RECIPE_INC"
