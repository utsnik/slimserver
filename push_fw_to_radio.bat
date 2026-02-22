@echo off
set RADIO_IP=10.1.1.60
set BUILD_SERVER=utking@10.1.4.12
echo Pushing fab4 firmware from build server to Squeezebox Radio at %RADIO_IP%...
ssh -o StrictHostKeyChecking=no -i C:\Users\Igland\.ssh\oracle_key %BUILD_SERVER% "scp -o StrictHostKeyChecking=no /home/utking/squeezeos-build/src/poky/build/tmp-fab4/deploy/images/fab4.bin root@%RADIO_IP%:/tmp/fab4.bin && ssh -o StrictHostKeyChecking=no root@%RADIO_IP% '/etc/init.d/rc.jive stop && /usr/bin/upgrade /tmp/fab4.bin'"
echo Push complete. The Radio should reboot shortly.
