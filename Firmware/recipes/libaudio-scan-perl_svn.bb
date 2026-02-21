DESCRIPTION = "Audio::Scan - Fast C scanning of audio file metadata"
SECTION = "libs"
LICENSE = "GPL"
PV = "0.93"
PR = "r29"

FULL_OPTIMIZATION = "-fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb -feliminate-unused-debug-types"

ARM_INSTRUCTION_SET = "arm"

SRC_URI = "http://cpan.metacpan.org/authors/id/A/AG/AGRUNDMA/Audio-Scan-0.93.tar.gz;md5sum=afcdbf8641e1a572a387fe097e3897ee;sha256sum=5a92f4fce0c5dc3f4f76b2266d484466ff6dfc64340371c392e678324465dc0e"

S = "${WORKDIR}/Audio-Scan-0.93"

inherit cpan

export INCLUDE = "${STAGING_LIBDIR}/../include"

FILES_${PN}-dbg = "${PERLLIBDIRS}/auto/Audio/Scan/.debug"
FILES_${PN} = "${PERLLIBDIRS}"
