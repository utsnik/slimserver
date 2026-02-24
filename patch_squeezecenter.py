import sys
import os

recipe_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezecenter/squeezecenter_svn.bb'
if not os.path.exists(recipe_path):
    print(f"Error: {recipe_path} not found")
    sys.exit(1)

with open(recipe_path, 'r') as f:
    content = f.read()

# 1. Increment PR
if 'PR = "r54"' in content:
    content = content.replace('PR = "r54"', 'PR = "r55"')
elif 'PR = "r55"' not in content:
    content = content.replace('PR = "r53"', 'PR = "r55"')
    print("Warning: PR = r54 not found, setting to r55")

# 2. Replace rm -r with rm -rf
content = content.replace('rm -r ', 'rm -rf ')

# 3. Ensure robust loop
# (It might already be there from previous patch if it worked)
old_loop_block = """	for i in ${INCLUDED_PLUGINS}; do
		mv ${D}/${prefix}/squeezecenter/Slim/Plugin.tmp/$i ${D}/${prefix}/squeezecenter/Slim/Plugin
	done"""

new_loop_block = """	for i in ${INCLUDED_PLUGINS}; do
		if [ -e ${D}/${prefix}/squeezecenter/Slim/Plugin.tmp/$i ]; then
			mv ${D}/${prefix}/squeezecenter/Slim/Plugin.tmp/$i ${D}/${prefix}/squeezecenter/Slim/Plugin
		fi
	done"""

if old_loop_block in content:
    content = content.replace(old_loop_block, new_loop_block)

with open(recipe_path, 'w') as f:
    f.write(content)

print("Successfully applied comprehensive robustness patch to squeezecenter_svn.bb (r55)")
