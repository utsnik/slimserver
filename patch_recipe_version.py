import sys
import os

recipe_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/images/squeezeos-image-boot.bb'
if not os.path.exists(recipe_path):
    print(f"Error: {recipe_path} not found")
    sys.exit(1)

# Completely clean version of the recipe
clean_recipe = """DESCRIPTION = "SqueezeOS - minimal bootable image"
PACKAGE_ARCH = "${MACHINE_ARCH}"
DEPENDS = "virtual/kernel"
PR = "r1"

inherit image squeezeos-upgrade-image

do_rootfs[depends] += "squeezeplay:do_make_squeezeos_squeezeplay_revision"

IMAGE_INSTALL += " \\
	squeezeos-base-files \\
	busybox \\
	udev \\
	mtd-utils \\
	ubi-utils"

IMAGE_LINGUAS = " "

# remove not needed ipkg informations
ROOTFS_POSTPROCESS_COMMAND += "remove_packaging_data_files"

# write squeezeos.version file
do_rootfs_prepend() {
	echo "${DISTRO_RELEASE} r${@open(os.path.join(bb.data.getVar('STAGING_DIR_TARGET', d, 1), 'squeezeos_squeezeplay_revision'), 'r').readline().strip()}" > ${IMAGE_ROOTFS}/etc/squeezeos.version
	echo `whoami`@`hostname` `date` >> ${IMAGE_ROOTFS}/etc/squeezeos.version
	echo "Base build revision: " ${METADATA_REVISION} >> ${IMAGE_ROOTFS}/etc/squeezeos.version
}

do_rm_work() {
	true
}
"""

with open(recipe_path, 'w') as f:
    f.write(clean_recipe)

print("Successfully restored and inlined squeezeos-image-boot.bb")
