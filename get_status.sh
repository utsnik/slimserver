#!/bin/bash
LOG_FILE="squeezeos-build/build.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "Log file not found at $LOG_FILE"
    exit 1
fi

# Try standard tail
if command -v tail >/dev/null 2>&1; then
    tail -n 20 "$LOG_FILE"
    exit 0
fi

# Try busybox tail
if command -v busybox >/dev/null 2>&1; then
    busybox tail -n 20 "$LOG_FILE"
    exit 0
fi

# Try sed (slow for huge files but standard)
sed -e :a -e '$q;N;21,$D;ba' "$LOG_FILE"
