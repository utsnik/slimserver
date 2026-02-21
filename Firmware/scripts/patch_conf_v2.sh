#!/bin/bash
CONF="squeezeos-build/src/poky/meta-squeezeos/conf/distro/squeezeos.conf"

REVISION_SQUEEZEPLAY="ae184c526fc5ba0f09132b8deb871ea85fecc04c"
REVISION_SQUEEZEOS="be98c690b6110be6535c63a4da5b8890310a0410"

# Fix the typo from previous run and ensure all are replaced
sed -i "s/SRCREV_pn-linux-imx25 ?= .*/SRCREV_pn-linux-imx25 ?= \"$REVISION_SQUEEZEOS\"/" "$CONF"
sed -i "s/SRCREV_pn-linux-fab4 ?= .*/SRCREV_pn-linux-fab4 ?= \"$REVISION_SQUEEZEOS\"/" "$CONF"
sed -i "s/SRCREV_pn-linux-jive ?= .*/SRCREV_pn-linux-jive ?= \"$REVISION_SQUEEZEOS\"/" "$CONF"
sed -i "s/SRCREV_pn-jivetest ?= .*/SRCREV_pn-jivetest ?= \"$REVISION_SQUEEZEOS\"/" "$CONF"
sed -i "s/SRCREV_pn-marvell-sdio-module-src = .*/SRCREV_pn-marvell-sdio-module-src = \"$REVISION_SQUEEZEOS\"/" "$CONF"

# Fix Audio::Scan which now uses CPAN but might still be referenced
sed -i "s/SRCREV_pn-libaudio-scan-perl ?= .*/SRCREV_pn-libaudio-scan-perl ?= \"\"/" "$CONF"

# Update Freetype preference to 2.4.2 which exists in meta-squeezeos
sed -i "s/PREFERRED_VERSION_freetype ?= \"2.1.10\"/PREFERRED_VERSION_freetype ?= \"2.4.2\"/" "$CONF"

echo "SRCREVs and Freetype version corrected in $CONF"
grep "SRCREV_pn" "$CONF"
grep "PREFERRED_VERSION_freetype" "$CONF"
