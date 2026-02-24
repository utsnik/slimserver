import sys
import os
import re

class_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/classes/squeezeos-upgrade-image.bbclass'
staging_path = '/home/utking/squeezeos-build/src/poky/build/tmp-fab4/staging/fab4-none-linux-gnueabi/squeezeos_squeezeplay_revision'

if not os.path.exists(class_path):
    print(f"Error: {class_path} not found")
    sys.exit(1)

# Try to get the real revision first from the staging area
revision = "unknown"
if os.path.exists(staging_path):
    with open(staging_path, 'r') as f:
        revision = f.readline().strip()
print(f"Detected revision: {revision}")

with open(class_path, 'r') as f:
    content = f.read()

# 1. Catch the specific hardcoded path and fix it
# The error was: cp: cannot stat `/home/squeezeos/poky/build/tmp-fab4/rootfs/etc/squeezeos.version': No such file or directory
failing_path = '/home/squeezeos/poky/build/tmp-fab4/rootfs/etc/squeezeos.version'
correct_path = '${IMAGE_ROOTFS}/etc/squeezeos.version'

content = content.replace(failing_path, correct_path)

# 2. Catch any other similarly hardcoded paths ending in rootfs/etc/squeezeos.version
content = re.sub(r'/[^ \n"]+/rootfs/etc/squeezeos\.version', correct_path, content)

# 3. Hardcode the version string if it was missed
content = content.replace('${@squeezeos_squeezeplay_revision(d)}', revision)

with open(class_path, 'w') as f:
    f.write(content)

print(f"Successfully applied precision path ({correct_path}) and revision ({revision}) patch")
