#!/bin/bash
CONF="squeezeos-build/src/poky/meta-squeezeos/conf/distro/squeezeos.conf"

REVISION_SQUEEZEPLAY="ae184c526fc5ba0f09132b8deb871ea85fecc04c"
REVISION_SQUEEZEOS="be98c690b6110be6535c63a4da5b8890310a0410"

# Replace AUTOREV for SqueezePlay components
sed -i "s/SRCREV_pn-squeezeplay ?= \"\${AUTOREV}\"/SRCREV_pn-squeezeplay ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-squeezeplay-baby ?= \"\${AUTOREV}\"/SRCREV_pn-squeezeplay-baby ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-squeezeplay-fab4 ?= \"\${AUTOREV}\"/SRCREV_pn-squeezeplay-fab4 ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-squeezeplay-jive ?= \"\${AUTOREV}\"/SRCREV_pn-squeezeplay-jive ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-squeezeplay-squeezeos ?= \"\${AUTOREV}\"/SRCREV_pn-squeezeplay-squeezeos ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"

sed -i "s/SRCREV_pn-libsdl-image ?= \"\${AUTOREV}\"/SRCREV_pn-libsdl-image ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-libsdl ?= \"\${AUTOREV}\"/SRCREV_pn-libsdl ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-libsdl-ttf ?= \"\${AUTOREV}\"/SRCREV_pn-libsdl-ttf ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-libsdl-gfx ?= \"\${AUTOREV}\"/SRCREV_pn-libsdl-gfx ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-freefont ?= \"\${AUTOREV}\"/SRCREV_pn-freefont ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"

sed -i "s/SRCREV_pn-luaprofiler ?= \"\${AUTOREV}\"/SRCREV_pn-luaprofiler ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-luasocket ?= \"\${AUTOREV}\"/SRCREV_pn-luasocket ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-lualoop ?= \"\${AUTOREV}\"/SRCREV_pn-lualoop ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-luajson ?= \"\${AUTOREV}\"/SRCREV_pn-luajson ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-luafilesystem ?= \"\${AUTOREV}\"/SRCREV_pn-luafilesystem ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-luazipfilter ?= \"\${AUTOREV}\"/SRCREV_pn-luazipfilter ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-lua ?= \"\${AUTOREV}\"/SRCREV_pn-lua ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-lua-native ?= \"\${AUTOREV}\"/SRCREV_pn-lua-native ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-luatolua++ ?= \"\${AUTOREV}\"/SRCREV_pn-luatolua++ ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-luamd5 ?= \"\${AUTOREV}\"/SRCREV_pn-luamd5 ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-luaexpat ?= \"\${AUTOREV}\"/SRCREV_pn-luaexpat ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-luartmp ?= \"\${AUTOREV}\"/SRCREV_pn-luartmp ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"

# Replace AUTOREV for SqueezeCenter
sed -i "s/SRCREV_pn-squeezecenter ?= \"\${AUTOREV}\"/SRCREV_pn-squeezecenter ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"
sed -i "s/SRCREV_pn-squeezecenter_full ?= \"\${AUTOREV}\"/SRCREV_pn-squeezecenter_full ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"

# Replace AUTOREV for SqueezeOS components
sed -i "s/SRCREV_pn-linux-imx25 ?= \"\${AUTOREV}\"/SRCREV_pn-linux-imx25 ?= \"$REVISION_SQUEEOS\"/" "$CONF"
sed -i "s/SRCREV_pn-linux-fab4 ?= \"\${AUTOREV}\"/SRCREV_pn-linux-fab4 ?= \"$REVISION_SQUEEOS\"/" "$CONF"
sed -i "s/SRCREV_pn-linux-jive ?= \"\${AUTOREV}\"/SRCREV_pn-linux-jive ?= \"$REVISION_SQUEEOS\"/" "$CONF"
sed -i "s/SRCREV_pn-jivetest ?= \"\${AUTOREV}\"/SRCREV_pn-jivetest ?= \"$REVISION_SQUEEOS\"/" "$CONF"
sed -i "s/SRCREV_pn-marvell-sdio-module-src = \"\${AUTOREV}\"/SRCREV_pn-marvell-sdio-module-src = \"$REVISION_SQUEEOS\"/" "$CONF"

# Replace AUTOREV for Tremor
sed -i "s/SRCREV_pn-tremor ?= \"\${AUTOREV}\"/SRCREV_pn-tremor ?= \"$REVISION_SQUEEZEPLAY\"/" "$CONF"

echo "SRCREVs patched in $CONF"
grep "SRCREV_pn" "$CONF" | head -n 5
