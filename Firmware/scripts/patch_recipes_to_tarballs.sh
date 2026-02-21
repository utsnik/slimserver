#!/bin/bash
PKGS="squeezeos-build/src/poky/meta-squeezeos/packages"

# Patch LibSDL recipes
sed -i 's|${SQUEEZEPLAY_SCM};module=SDL-${BV}|file://SDL-${BV}.tar.gz|' "$PKGS/libsdl/libsdl_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=SDL_image-${BV}|file://SDL_image-${BV}.tar.gz|' "$PKGS/libsdl/libsdl-image_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=SDL_ttf-${BV}|file://SDL_ttf-${BV}.tar.gz|' "$PKGS/libsdl/libsdl-ttf_svn.bb"
sed -i 's|${SQUEEZEPLAY_SCM};module=SDL_gfx-${BV}|file://SDL_gfx-${BV}.tar.gz|' "$PKGS/libsdl/libsdl-gfx_svn.bb"

# Patch Lua recipe
sed -i 's|${SQUEEZEPLAY_SCM};module=lua-${BV}|file://lua-${BV}.tar.gz|' "$PKGS/lua/lua.inc"

# Patch Freefont recipe
sed -i 's|${SQUEEZEPLAY_SCM};module=freefont-${BV}|file://freefont-${BV}.tar.gz|' "$PKGS/freefont/freefont_svn.bb"

# Patch Squeezeplay recipe
sed -i 's|${SQUEEZEPLAY_SCM};module=squeezeplay|file://squeezeplay.tar.gz|' "$PKGS/squeezeplay/squeezeplay_svn.bb"

echo "Recipes patched to use local tarballs."
grep -r "file://" "$PKGS" | grep "tar.gz" | head -n 10
