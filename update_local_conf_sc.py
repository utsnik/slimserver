import os

conf_path = '/home/utking/squeezeos-build/src/build/conf/local.conf'

if not os.path.exists(conf_path):
    print(f"Error: {conf_path} not found")
    exit(1)

with open(conf_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'SQUEEZECENTER_SCM =' in line or \
       'SQUEEZECENTER_SCM ?=' in line or \
       'SRCREV_pn-squeezecenter =' in line:
        continue
    new_lines.append(line)

new_lines.append('SQUEEZECENTER_SCM = "git://github.com/Logitech/slimserver.git;protocol=https;branch=public/7.8"\n')
new_lines.append('SRCREV_pn-squeezecenter = "da8d20eddeb5beac1a6d49f4cf1101ad6f1e8a96"\n')

with open(conf_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully injected SQUEEZECENTER_SCM and SRCREV_pn-squeezecenter overrides")
