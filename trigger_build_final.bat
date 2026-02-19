@echo off
echo Starting Remote Build...
ssh -o StrictHostKeyChecking=no -i C:\Users\Igland\.ssh\oracle_key utking@10.1.4.12 "cd squeezeos-build/src/docker && docker build -t squeezeos_builder . && cd .. && nohup docker run --rm -v /home/utking/squeezeos-build/src:/home/squeezeos/ squeezeos_builder /bin/bash -c 'source /home/squeezeos/poky/poky-init-build-env; bitbake squeezeos-image' > build.log 2>&1 &"
echo Build command sent via SSH.
