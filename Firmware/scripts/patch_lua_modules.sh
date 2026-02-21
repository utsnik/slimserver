#!/bin/bash
PKGS="squeezeos-build/src/poky/meta-squeezeos/packages/lua"

# Create files directory if not exists (should exist from previous)
mkdir -p "$PKGS/files"

# Move created tarballs
mv squeezeos-build/src/poky/sources/tolua++-1.0.92.tar.gz "$PKGS/files/"
mv squeezeos-build/src/poky/sources/luafilesystem-1.2.tar.gz "$PKGS/files/"
mv squeezeos-build/src/poky/sources/luasocket-2.0.2.tar.gz "$PKGS/files/"
mv squeezeos-build/src/poky/sources/luaprofiler-2.0.tar.gz "$PKGS/files/"
mv squeezeos-build/src/poky/sources/luajson.tar.gz "$PKGS/files/"
mv squeezeos-build/src/poky/sources/luamd5.tar.gz "$PKGS/files/"
mv squeezeos-build/src/poky/sources/luazipfilter.tar.gz "$PKGS/files/"
mv squeezeos-build/src/poky/sources/luaexpat-1.0.2.tar.gz "$PKGS/files/"

# Patch recipes
sed -i 's|${SQUEEZEPLAY_SCM};module=tolua++-${BV}|file://tolua++-${BV}.tar.gz|' "$PKGS/luatolua++_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=luafilesystem-${BV}|file://luafilesystem-${BV}.tar.gz|' "$PKGS/luafilesystem_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=luasocket-${BV}|file://luasocket-${BV}.tar.gz|' "$PKGS/luasocket_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=luaprofiler-${BV}|file://luaprofiler-${BV}.tar.gz|' "$PKGS/luaprofiler_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=luajson|file://luajson.tar.gz|' "$PKGS/luajson_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=luamd5|file://luamd5.tar.gz|' "$PKGS/luamd5_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=luazipfilter|file://luazipfilter.tar.gz|' "$PKGS/luazipfilter_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=luaexpat-${BV}|file://luaexpat-${BV}.tar.gz|' "$PKGS/luaexpat_svn.bb"

echo "All Lua module recipes patched and tarballs moved."
ls -l "$PKGS/files/"
grep "file://" "$PKGS/"*_svn.bb
