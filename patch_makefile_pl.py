import sys
import os

makefile_pl = 'Makefile.PL'
if not os.path.exists(makefile_pl):
    print(f"Error: {makefile_pl} not found")
    sys.exit(1)

with open(makefile_pl, 'r') as f:
    content = f.read()

# Mock DBI and DBI::DBD
mock_code = """
my $DBI_required = 0; 
eval 'package DBI; sub VERSION { 1.616 }';
eval 'package DBI::DBD; sub dbd_postamble { 
    my $xst = "/home/squeezeos/poky/build/tmp-fab4/staging/x86_64-linux/usr/lib/perl/5.10.0/auto/DBI/Driver.xst";
    return "SQLite.xsi: $xst\\n\\t\\$(PERL) -p -e \\"s/~DRIVER~/SQLite/g\\" $xst > SQLite.xsi\\n";
}';
"""

# Replace the first 'require DBI;' or similar
new_content = content.replace('require DBI;', mock_code, 1)
# Also handle the second occurrence in MY::postamble
new_content = new_content.replace('require DBI;', '#require DBI;', 1)
new_content = new_content.replace('require DBI::DBD;', '#require DBI::DBD;', 1)

with open(makefile_pl, 'w') as f:
    f.write(new_content)

print("Successfully patched Makefile.PL")
