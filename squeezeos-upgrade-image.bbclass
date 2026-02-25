# SqueezeOS upgrade image creation

# Image processing:
# 1. Create a zip file with the kernel (zImage), the rootfs and some metadata files.
# 2. Add an md5sum for the kernel and the rootfs.
# 3. Create a version file.

IMAGE_SQUEEZEOS_BOARD_VERSION ?= "10"
IMAGE_SQUEEZEOS_EXTRA_VERSION ?= ""

do_squeezeos_image() {
	# Create a temporary directory
	tmpdir=`mktemp -d`
	if [ -z "${tmpdir}" ]; then
		echo "Failed to create temporary directory"
		exit 1
	fi

	# Copy files
	cp ${DEPLOY_DIR_IMAGE}/zImage-${MACHINE}.bin ${tmpdir}/zImage${IMAGE_SQUEEZEOS_EXTRA_VERSION}
	cp ${DEPLOY_DIR_IMAGE}/${ROOTFS_IMAGE_NAME} ${tmpdir}/root.cramfs

	# Try deploy dir first (survives rootfs purge), then rootfs
	if [ -e ${DEPLOY_DIR_IMAGE}/squeezeos.version ]; then
		cp ${DEPLOY_DIR_IMAGE}/squeezeos.version ${tmpdir}/jive.version
	elif [ -e ${IMAGE_ROOTFS}/etc/squeezeos.version ]; then
		cp ${IMAGE_ROOTFS}/etc/squeezeos.version ${tmpdir}/jive.version
	else
		echo "7.8 runknown" > ${tmpdir}/jive.version
	fi

	echo -e ${IMAGE_SQUEEZEOS_BOARD_VERSION} > ${tmpdir}/board.version

	# Prepare files
	cd ${tmpdir}
	md5sum zImage${IMAGE_SQUEEZEOS_EXTRA_VERSION} root.cramfs  > upgrade.md5

	VERSION=${DISTRO_RELEASE}_runknown

	# Create zip
	rm -f ${DEPLOY_DIR_IMAGE}/${MACHINE}_${VERSION}.bin
	zip ${DEPLOY_DIR_IMAGE}/${MACHINE}_${VERSION}.bin jive.version board.version upgrade.md5 zImage${IMAGE_SQUEEZEOS_EXTRA_VERSION} root.cramfs
	cd ${DEPLOY_DIR_IMAGE}

	rm -f ${MACHINE}.bin
	ln -s ${MACHINE}_${VERSION}.bin ${MACHINE}.bin

	# Cleanup
	rm -rf ${tmpdir}
}

addtask squeezeos_image after do_rootfs before do_build


python squeezeos_version() {
    import os, bb, datetime

    staging = bb.data.getVar('STAGING_DIR_TARGET', d, 1)
    rootfs = bb.data.getVar('IMAGE_ROOTFS', d, 1)
    deploy = bb.data.getVar('DEPLOY_DIR_IMAGE', d, 1)
    distro_release = bb.data.getVar('DISTRO_RELEASE', d, 1)
    metadata_revision = bb.data.getVar('METADATA_REVISION', d, 1)

    try:
        rev_file = os.path.join(staging, 'squeezeos_squeezeplay_revision')
        revision = open(rev_file, 'r').readline().strip()
    except:
        revision = "unknown"

    version_str = "%s r%s" % (distro_release, revision)
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = "%s\nbuild@builder %s\nBase build revision: %s\n" % (version_str, now_str, metadata_revision)

    # Write to rootfs for the device
    os.makedirs(os.path.join(rootfs, 'etc'), exist_ok=True)
    for dest in [os.path.join(rootfs, 'etc', 'squeezeos.version'),
                 os.path.join(deploy, 'squeezeos.version')]:
        try:
            fh = open(dest, 'w')
            fh.write(content)
            fh.close()
        except Exception:
            pass
}
