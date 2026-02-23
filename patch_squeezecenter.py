import sys
import os

recipe_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezecenter/squeezecenter_svn.bb'
if not os.path.exists(recipe_path):
    print(f"Error: {recipe_path} not found")
    sys.exit(1)

with open(recipe_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'INCLUDED_PLUGINS += "Amazon Classical Deezer"' in line:
        new_lines.append('# ' + line)
    else:
        new_lines.append(line)

with open(recipe_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully patched squeezecenter_svn.bb")
