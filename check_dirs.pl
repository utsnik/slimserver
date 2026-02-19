use strict;
use lib '/lms';
# Fake initialization
use Slim::Utils::OSDetect;
Slim::Utils::OSDetect::init();
print "------ PLUGIN DIRS START ------\n";
my @dirs = Slim::Utils::OSDetect::dirsFor('Plugins');
foreach my $d (@dirs) {
    print "$d\n";
}
print "------ PLUGIN DIRS END ------\n";
