import os

bb_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/dhcp-forwarder/dhcp-forwarder_0.8.bb'

if not os.path.exists(bb_path):
    print(f"Error: {bb_path} not found")
    exit(1)

with open(bb_path, 'r') as f:
    content = f.read()

content = content.replace(
    'http://savannah.nongnu.org/download/dhcp-fwd/dhcp-forwarder-${PV}.tar.bz2',
    'file:///home/squeezeos/poky/sources/dhcp-forwarder-${PV}.tar.bz2'
)

with open(bb_path, 'w') as f:
    f.write(content)

print("Successfully patched dhcp-forwarder_0.8.bb with precise string replacement")
