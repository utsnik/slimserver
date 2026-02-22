import os

conf_path = '/home/utking/squeezeos-build/src/build/conf/local.conf'

if not os.path.exists(conf_path):
    print(f"Error: {conf_path} not found")
    exit(1)

with open(conf_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Remove any previous entries related to my fixes
    if '# SqueezeOS Build Patch Overrides' in line or \
       'DL_DIR =' in line or \
       'GIT =' in line or \
       'PREMIRRORS' in line or \
       'http://downloads.sourceforge.net/fuse/fuse-2.7.2.tar.gz' in line:
        continue
    new_lines.append(line)

# Add definitive overrides
new_lines.append('\n# SqueezeOS Build Patch Overrides\n')
new_lines.append('DL_DIR = "/home/squeezeos/poky/sources"\n')
new_lines.append('GIT = "/home/squeezeos/git_wrapper.sh"\n')
# Force fuse to use the local mirror
new_lines.append('PREMIRRORS_append = " http://downloads.sourceforge.net/fuse/.* file:///home/squeezeos/poky/sources/ \\n "\n')

with open(conf_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully updated local.conf with PREMIRRORS for fuse")
