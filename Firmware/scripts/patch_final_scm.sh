#!/bin/bash
PKGS="squeezeos-build/src/poky/meta-squeezeos/packages"

# Create files directories if needed
mkdir -p "$PKGS/tremor/files"
mkdir -p "$PKGS/portaudio/files"
mkdir -p "$PKGS/lua/files"
mkdir -p "$PKGS/squeezeplay/files"

# Move tarballs
mv squeezeos-build/src/poky/sources/Tremor.tar.gz "$PKGS/tremor/files/"
mv squeezeos-build/src/poky/sources/portaudio_v19_1360.tar.gz "$PKGS/portaudio/files/"
mv squeezeos-build/src/poky/sources/loop-2.2-alpha.tar.gz "$PKGS/lua/files/"
mv squeezeos-build/src/poky/sources/luartmp-squeezeplay.tar.gz "$PKGS/lua/files/"
mv squeezeos-build/src/poky/sources/squeezeplay_fab4.tar.gz "$PKGS/squeezeplay/files/"
mv squeezeos-build/src/poky/sources/squeezeplay_baby.tar.gz "$PKGS/squeezeplay/files/"
mv squeezeos-build/src/poky/sources/squeezeplay_squeezeos.tar.gz "$PKGS/squeezeplay/files/"
mv squeezeos-build/src/poky/sources/squeezeplay_jive.tar.gz "$PKGS/squeezeplay/files/"

# Patch recipes
sed -i 's|${SQUEEZEPLAY_SCM};module=Tremor|file://Tremor.tar.gz|' "$PKGS/tremor/tremor_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=portaudio_${BV}|file://portaudio_${BV}.tar.gz|' "$PKGS/portaudio/portaudio_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=loop-${BV}|file://loop-${BV}.tar.gz|' "$PKGS/lua/lualoop_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=luartmp-squeezeplay|file://luartmp-squeezeplay.tar.gz|' "$PKGS/lua/luartmp_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=squeezeplay_fab4|file://squeezeplay_fab4.tar.gz|' "$PKGS/squeezeplay/squeezeplay-fab4_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=squeezeplay_baby|file://squeezeplay_baby.tar.gz|' "$PKGS/squeezeplay/squeezeplay-baby_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=squeezeplay_squeezeos|file://squeezeplay_squeezeos.tar.gz|' "$PKGS/squeezeplay/squeezeplay-squeezeos_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=squeezeplay_jive|file://squeezeplay_jive.tar.gz|' "$PKGS/squeezeplay/squeezeplay-jive_svn.bb"

echo "All remaining SQUEEZEPLAY_SCM recipes patched and tarballs moved."
grep "file://" "$PKGS/"*/*_svn.bb | grep "tar.gz"
