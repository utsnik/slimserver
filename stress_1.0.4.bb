DESCRIPTION = "stress"
SECTION = "bin"
LICENSE = "GPL"

#PR = "r0"

SRC_URI="file://stress-${PV}.tar.gz"

S = "${WORKDIR}/stress-${PV}"

inherit autotools

PACKAGES = "stress"
FILES_${PN} = "${bindir}/*"
