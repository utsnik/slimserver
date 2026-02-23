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

new_lines.append('SQUEEZECENTER_SCM = "git://10.1.4.164/slimserver_mirror.git;protocol=git;branch=public/9.1"\n')
new_lines.append('SRCREV_pn-squeezecenter = "4967db209310c083db57f70d94e90802d655e973"\n')

with open(conf_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully injected SQUEEZECENTER_SCM local git daemon override for isolated mirror")
