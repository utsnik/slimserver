import os

bb_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/dhcp-forwarder/dhcp-forwarder_0.8.bb'

if not os.path.exists(bb_path):
    print(f"Error: {bb_path} not found")
    exit(1)

with open(bb_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('SRC_URI ='):
        new_lines.append('SRC_URI = "file:///home/squeezeos/poky/sources/dhcp-forwarder-${PV}.tar.bz2"\n')
    else:
        new_lines.append(line)

with open(bb_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully patched dhcp-forwarder_0.8.bb to use local file source")
