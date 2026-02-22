import os

conf_path = '/home/utking/squeezeos-build/src/build/conf/local.conf'

if not os.path.exists(conf_path):
    print(f"Error: {conf_path} not found")
    exit(1)

with open(conf_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Remove any SQUEEZEOS_SVN or SQUEEZEPLAY_SCM or GIT overrides I added
    if '# Direct fetch from GitHub' in line or \
       'SQUEEZEOS_SVN =' in line or \
       'SQUEEZEPLAY_SCM =' in line or \
       'GIT =' in line or \
       '# Fix git fetch' in line:
        continue
    new_lines.append(line)

with open(conf_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully cleaned local.conf")
