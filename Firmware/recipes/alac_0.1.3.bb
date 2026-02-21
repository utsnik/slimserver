DESCRIPTION = "Simple Apple Lossless Decoder"
SECTION = "libs"
LICENSE = "LGPL"

PR="r2"

SRC_URI = "git://github.com/macosforge/alac.git;protocol=https;branch=master"

S="${WORKDIR}/git/codec"


do_make() { 
	oe_runmake
} 

do_install() { 
	mkdir -p ${D}/usr/bin
	cp ${S}/alac ${D}/usr/bin
}
	
FILES_${PN} = "/usr/bin/alac"
