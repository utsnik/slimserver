#!/bin/bash
if [ -f squeezeos-build/build.log ]; then
    tail -n 20 squeezeos-build/build.log
else
    echo "Log file not found yet."
fi
