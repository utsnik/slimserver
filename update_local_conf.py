import os

conf_path = '/home/utking/squeezeos-build/src/build/conf/local.conf'

if not os.path.exists(conf_path):
    print(f"Error: {conf_path} not found")
    exit(1)

with open(conf_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Remove any SQUEEZEOS_SVN or SQUEEZEPLAY_SCM or GIT overrides or broken PREMIRRORS
    if '# Direct fetch from GitHub' in line or \
       'SQUEEZEOS_SVN =' in line or \
       'SQUEEZEPLAY_SCM =' in line or \
       'GIT =' in line or \
       '# Fix git fetch' in line or \
       'DL_DIR =' in line or \
       'PREMIRRORS_append =' in line or \
       '# SqueezeOS Build Patch Overrides' in line:
        continue
    new_lines.append(line)

# Add ONLY the working overrides (absolute DL_DIR and GIT wrapper)
new_lines.append('\n# SqueezeOS Build Patch Overrides\n')
new_lines.append('DL_DIR = "/home/squeezeos/poky/sources"\n')
new_lines.append('GIT = "/home/squeezeos/git_wrapper.sh"\n')

with open(conf_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully cleaned local.conf of broken PREMIRRORS")
