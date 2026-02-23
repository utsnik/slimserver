import sys
import os

makefile_pl = 'Makefile.PL'
if not os.path.exists(makefile_pl):
    sys.stderr.write("Error: Makefile.PL not found\n")
    sys.exit(1)

with open(makefile_pl, 'r') as f:
    content = f.read()

# Mock DBI and DBI::DBD
# We use standard string concatenation for compatibility
DRIVER_XST = "/home/squeezeos/poky/build/tmp-fab4/staging/x86_64-linux/usr/lib/perl/5.10.0/auto/DBI/Driver.xst"
mock_code = '\nmy $DBI_required = 0; \neval \'package DBI; sub VERSION { 1.616 }\';\neval \'package DBI::DBD; sub dbd_postamble { \n    my $xst = "' + DRIVER_XST + '";\n    return "SQLite.xsi: $xst\\n\\t\\$(PERL) -p -e \\"s/~DRIVER~/SQLite/g\\" $xst > SQLite.xsi\\n";\n}\';\n'

# Replace the first 'require DBI;' or similar
if 'require DBI;' in content:
    new_content = content.replace('require DBI;', mock_code, 1)
    # Also handle the second occurrence in MY::postamble if it exists
    new_content = new_content.replace('require DBI;', '#require DBI;', 1)
else:
    # If already patched or variant found, try to be robust
    new_content = content

new_content = new_content.replace('require DBI::DBD;', '#require DBI::DBD;')

with open(makefile_pl, 'w') as f:
    f.write(new_content)

sys.stdout.write("Successfully patched Makefile.PL\n")
