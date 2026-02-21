#!/bin/bash
nohup bash squeezeos-build/remote_build.sh > build.log 2>&1 &
echo "Build launched in background. Check build.log for progress."
