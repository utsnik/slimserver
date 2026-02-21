#!/bin/bash
CONF="squeezeos-build/src/poky/meta-squeezeos/conf/distro/squeezeos.conf"

REPO_SQUEEZEPLAY="/home/squeezeos/poky/sources/git/github.com.ralph-irving.squeezeos-squeezeplay.git"
REPO_SQUEEZEOS="/home/squeezeos/poky/sources/git/github.com.ralph-irving.squeezeos.git"

# Override SCM URLs to point to local git clones
sed -i "s|SQUEEZEOS_SVN ?= .*|SQUEEZEOS_SVN ?= \"git://$REPO_SQUEEZEOS;branch=public/\${DISTRO_VERSION};repopath=src;protocol=file\"|" "$CONF"
sed -i "s|SQUEEZEPLAY_SCM ?= .*|SQUEEZEPLAY_SCM ?= \"git://$REPO_SQUEEZEPLAY;branch=public/\${DISTRO_VERSION};repopath=src;protocol=file\"|" "$CONF"

echo "SCM URLs updated to local paths in $CONF"
grep -E "SQUEEZEOS_SVN|SQUEEZEPLAY_SCM" "$CONF"
