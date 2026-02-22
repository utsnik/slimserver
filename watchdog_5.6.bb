DESCRIPTION = "System watchdog daemon"
LICENSE = "GPL"
PR = "r5"

SRC_URI = " \
	file://watchdog-${PV}.tar.gz \
	file://memory-buffers-cache.patch;patch=1 \
	file://watchdog-semaphore.patch;patch=1 \
	file://startup-delay.patch;patch=1 \
	"

inherit autotools

FILES_${PN} = "${sbindir}/watchdog"
