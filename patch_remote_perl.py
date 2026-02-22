import os

patch_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/perl/perl-native_5.10.0.bb'

if not os.path.exists(patch_path):
    print(f"Error: {patch_path} not found")
    exit(1)

with open(patch_path, 'r') as f:
    lines = f.readlines()

new_lines = []
found = False
for line in lines:
    if "config.sh > config.sh.new" in line:
        # Use a simpler sed that just works
        # We replace the entire sed line with one that adds libs='-lm'
        newline = "    sed 's!${STAGING_DIR}/bin!${STAGING_BINDIR}!;s!${STAGING_DIR}/lib!${STAGING_LIBDIR}!;s!^perllibs=!libs=\"-lm \"; perllibs=!' < config.sh > config.sh.new\n"
        new_lines.append(newline)
        found = True
    else:
        new_lines.append(line)

if found:
    with open(patch_path, 'w') as f:
        f.writelines(new_lines)
    print("Successfully patched perl-native recipe with robust libs definition.")
else:
    print("Error: Target pattern not found in recipe.")
    exit(1)
