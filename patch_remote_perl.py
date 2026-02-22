import os
import re

patch_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/perl/perl-native_5.10.0.bb'

if not os.path.exists(patch_path):
    print(f"Error: {patch_path} not found")
    exit(1)

with open(patch_path, 'r') as f:
    lines = f.readlines()

new_lines = []
found = False
for line in lines:
    if "s!${STAGING_DIR}/lib!${STAGING_LIBDIR}!" in line and "config.sh" in line:
        # Replace the broken line with the correct one
        newline = "         s!${STAGING_DIR}/lib!${STAGING_LIBDIR}!; s!^libs=''!libs=''-lm !' < config.sh > config.sh.new\n"
        new_lines.append(newline)
        found = True
    else:
        new_lines.append(line)

if found:
    with open(patch_path, 'w') as f:
        f.writelines(new_lines)
    print("Successfully fixed the syntax error in perl-native recipe.")
else:
    print("Error: Target pattern not found in recipe.")
    exit(1)
