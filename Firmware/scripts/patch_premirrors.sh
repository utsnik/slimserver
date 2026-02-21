#!/bin/bash
CONF="squeezeos-build/src/poky/build/conf/local.conf"

cat <<EOF >> "$CONF"

# Force usage of local git mirrors to bypass container fetch issues
SOURCE_MIRROR_URL = "file:///home/squeezeos/poky/sources/"
INHERIT += "own-mirrors"
PREMIRRORS_prepend = " \
git://github.com/.* git:///home/squeezeos/poky/sources/git/BASENAME \
https://github.com/.* git:///home/squeezeos/poky/sources/git/BASENAME \
"
EOF

echo "PREMIRRORS added to $CONF"
tail -n 10 "$CONF"
