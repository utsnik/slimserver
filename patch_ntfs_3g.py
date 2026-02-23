import os

bb_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/ntfs-3g/ntfs-3g_2009.4.4.bb'

if not os.path.exists(bb_path):
    print(f"Error: {bb_path} not found")
    exit(1)

with open(bb_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('SRC_URI ='):
        new_lines.append('SRC_URI = "file:///home/squeezeos/poky/sources/ntfs-3g-${PV}.tgz"\n')
    else:
        new_lines.append(line)

with open(bb_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully patched ntfs-3g_2009.4.4.bb to use local file source")
