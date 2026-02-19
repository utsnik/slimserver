#!/bin/bash
docker run --rm -v $(pwd)/squeezeos-build:/work -w /work alpine sh remote_patch.sh
