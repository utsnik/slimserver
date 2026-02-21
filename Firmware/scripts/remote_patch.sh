#!/bin/sh
set -e
apk add --no-cache patch
patch -p1 < radio_snappiness_safe.patch
