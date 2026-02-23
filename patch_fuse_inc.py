import os

inc_path = '/home/utking/squeezeos-build/src/poky/meta/packages/fuse/fuse.inc'

if not os.path.exists(inc_path):
    print(f"Error: {inc_path} not found")
    exit(1)

with open(inc_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('SRC_URI ='):
        new_lines.append('SRC_URI = "file:///home/squeezeos/poky/sources/fuse-${PV}.tar.gz"\n')
    else:
        new_lines.append(line)

with open(inc_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully patched fuse.inc to use local file source")
