#!/bin/bash
set -e
cd squeezeos-build/docker

echo "Building Docker Image..."
docker build -t squeezeos_builder .

echo "Running Firmware Build..."
# Run the build non-interactively
docker run --rm -v $(pwd)/../:/home/squeezeos/ squeezeos_builder /bin/bash -c "source /home/squeezeos/poky/poky-init-build-env; bitbake squeezeos-image"
