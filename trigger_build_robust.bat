@echo off
echo Starting Remote Build (Robust)...
ssh -o StrictHostKeyChecking=no -i C:\Users\Igland\.ssh\oracle_key utking@10.1.4.12 "export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin; cd squeezeos-build/src/docker && docker build -t squeezeos_builder . && cd .. && nohup docker run --rm -v /home/utking/squeezeos-build/src:/home/squeezeos/ squeezeos_builder /bin/bash -c 'whoami && mkdir -p /home/squeezeos/build && cd poky && source ./poky-init-build-env ../build && bitbake squeezeos-image' > /tmp/squeezeos_build.log 2>&1 &"
echo Robust build command sent via SSH.
