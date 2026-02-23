import os
import re

recipe_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/perl/libdbd-sqlite-perl_1.34.bb'

if not os.path.exists(recipe_path):
    print(f"Error: {recipe_path} not found")
    exit(1)

with open(recipe_path, 'r') as f:
    content = f.read()

# Define the fix
patch_prepend = """
do_configure_prepend() {
    export PERL5LIB="${STAGING_LIBDIR_NATIVE}/perl/5.10.0:$PERL5LIB"
    # Force use of native perl from staging
    export PATH="${STAGING_BINDIR_NATIVE}:$PATH"
}
"""

patch_configure = """
do_configure() {
    export PERL5LIB="${STAGING_LIBDIR_NATIVE}/perl/5.10.0:$PERL5LIB"
    yes '' | ${STAGING_BINDIR_NATIVE}/perl Makefile.PL ${EXTRA_CPANFLAGS}
    if [ "${BUILD_SYS}" != "${HOST_SYS}" ]; then
        . ${STAGING_DIR}/${TARGET_SYS}/perl/config.sh
        # local fix for DBD-SQLite
        sed -i -e "s:\(LDDLFLAGS.*\)${STAGING_LIBDIR_NATIVE}:\1${STAGING_LIBDIR}:" Makefile
    fi
}
"""

# Apply do_configure_prepend
if 'do_configure_prepend' in content:
    content = re.sub(r'do_configure_prepend\(\) \{.*?\}', patch_prepend.strip(), content, flags=re.DOTALL)
else:
    content += patch_prepend

# Apply do_configure
if 'do_configure' in content and 'cpan_do_configure' not in content:
     # If do_configure exists but is not from cpan (our previous attempt), replace it
     content = re.sub(r'do_configure\(\) \{.*?\}', patch_configure.strip(), content, flags=re.DOTALL)
elif 'do_configure' not in content:
    content += patch_configure

with open(recipe_path, 'w') as f:
    f.write(content)

print("Successfully updated libdbd-sqlite-perl with refined force-staged-perl fix")
