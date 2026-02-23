import os

recipe_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/perl/libdbd-sqlite-perl_1.34.bb'

if not os.path.exists(recipe_path):
    print(f"Error: {recipe_path} not found")
    exit(1)

with open(recipe_path, 'r') as f:
    content = f.read()

patch = """
do_configure_prepend() {
    export PERL5LIB="${STAGING_LIBDIR_NATIVE}/perl/5.10.0:$PERL5LIB"
}
"""

if 'do_configure_prepend' not in content:
    with open(recipe_path, 'w') as f:
        f.write(content + patch)
    print("Successfully patched libdbd-sqlite-perl with PERL5LIB export")
else:
    print("do_configure_prepend already exists in recipe")
