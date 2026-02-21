DESCRIPTION = "DBD::SQLite - SQLite driver for the Perl5 Database Interface (DBI)"
SECTION = "libs"
LICENSE = "Artistic|GPL"
PR = "r18"

FULL_OPTIMIZATION = "-fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb -feliminate-unused-debug-types"

ARM_INSTRUCTION_SET = "arm"

DEPENDS = "libdbi-perl libdbi-perl-native sqlite3"

SRC_URI = "http://cpan.metacpan.org/authors/id/A/AD/ADAMK/DBD-SQLite-1.34_01.tar.gz;md5sum=2583ad592bfc9ea443860c12c303b6b8;sha256sum=21e5ceced5fce0143b0035ac8d2cfb152e5b1ed1d426438ec47dac30ea5f36dc"

S = "${WORKDIR}/DBD-SQLite-1.34_01"

inherit cpan

FILES_${PN}-doc = "${PERLLIBDIRS}/*.pod"
FILES_${PN} = "${PERLLIBDIRS}"

cpan_do_install() {
        # from cpan class
        if [ yes = "yes" ]; then
                oe_runmake install_vendor
        fi

        # Remove unnecessary large source files
        rm -rf ${D}/${prefix}/lib/perl5/auto/share/dist/DBD-SQLite
}
