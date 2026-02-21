#!/bin/bash
BBCLASS="squeezeos-build/src/poky/meta/classes/base.bbclass"

# Move GIT_CONFIG to a local container path (/tmp) to avoid volume locking issues
sed -i 's|GIT_CONFIG = "${STAGING_DIR_NATIVE}/usr/etc/gitconfig"|GIT_CONFIG = "/tmp/bitbake-gitconfig"|' "$BBCLASS"

echo "GIT_CONFIG patched in $BBCLASS"
grep "GIT_CONFIG =" "$BBCLASS"
