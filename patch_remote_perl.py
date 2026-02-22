import os

patch_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/perl/perl-native_5.10.0.bb'

if not os.path.exists(patch_path):
    print(f"Error: {patch_path} not found")
    exit(1)

with open(patch_path, 'r') as f:
    content = f.read()

target = "s!${STAGING_DIR}/lib!${STAGING_LIBDIR}!' < config.sh"
replacement = "s!${STAGING_DIR}/lib!${STAGING_LIBDIR}!' ; s!^libs=''!libs=''-lm ! < config.sh"

if target in content:
    new_content = content.replace(target, replacement)
    with open(patch_path, 'w') as f:
        f.write(new_content)
    print("Successfully patched perl-native recipe.")
else:
    if replacement in content:
        print("Recipe already patched.")
    else:
        print("Error: Target string not found in recipe.")
        exit(1)
