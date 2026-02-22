DESCRIPTION="A simple command to run on Unix systems that will check the time \
and optionally drift compared with a known, local and reliable NTP \
time server." 
LICENSE = "individual"
PR = "r6"

SRC_URI = "file://msntp-1.6.tar.gz"

S = "${WORKDIR}"

export LIBS = "-lm"

PACKAGES = "msntp"

FILES_msntp = "${sbindir}/msntp"

do_compile() {
	${CC} ${CFLAGS} main.c unix.c internet.c socket.c timing.c libmsntp.c example.c -o msntp ${LDFLAGS} ${LIBS}
}

do_install () {
	# Install msntp
	install -m 0755 -d ${D}${sbindir}
	install -m 0755 ${S}/msntp ${D}${sbindir}/msntp
}
