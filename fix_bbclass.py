import os

staging_path = '/home/utking/squeezeos-build/src/poky/build/tmp-fab4/staging/fab4-none-linux-gnueabi/squeezeos_squeezeplay_revision'
class_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/classes/squeezeos-upgrade-image.bbclass'

try:
    with open(staging_path, 'r') as f:
        revision = f.readline().strip()
except Exception:
    revision = "unknown"

with open(class_path, 'r') as f:
    content = f.read()

# 1. Update do_squeezeos_image to read from DEPLOY_DIR_IMAGE instead of purged TMPDIR
content = content.replace(
    'cp ${TMPDIR}/rootfs/etc/squeezeos.version ${tmpdir}/jive.version',
    'if [ -f ${DEPLOY_DIR_IMAGE}/squeezeos.version ]; then cp ${DEPLOY_DIR_IMAGE}/squeezeos.version ${tmpdir}/jive.version; else echo "7.8 runknown" > ${tmpdir}/jive.version; fi'
)

# 2. Hardcode revision in zip file VERSION variable explicitly
content = content.replace(
    'VERSION=${DISTRO_RELEASE}_r${@squeezeos_squeezeplay_revision(d)}',
    f'VERSION=${{DISTRO_RELEASE}}_r{revision}'
)

# 3. Update squeezeos_version to hardcode revision AND copy the version file to DEPLOY_DIR_IMAGE
old_func = '''squeezeos_version() {
	echo "${DISTRO_RELEASE} r${@squeezeos_squeezeplay_revision(d)}" > ${IMAGE_ROOTFS}/etc/squeezeos.version
	echo `whoami`@`hostname` `date` >> ${IMAGE_ROOTFS}/etc/squeezeos.version
	echo "Base build revision: " ${METADATA_REVISION} >> ${IMAGE_ROOTFS}/etc/squeezeos.version
}'''

new_func = f'''squeezeos_version() {{
	echo "${{DISTRO_RELEASE}} r{revision}" > ${{IMAGE_ROOTFS}}/etc/squeezeos.version
	echo `whoami`@`hostname` `date` >> ${{IMAGE_ROOTFS}}/etc/squeezeos.version
	echo "Base build revision: " ${{METADATA_REVISION}} >> ${{IMAGE_ROOTFS}}/etc/squeezeos.version
	mkdir -p ${{DEPLOY_DIR_IMAGE}}
	cp ${{IMAGE_ROOTFS}}/etc/squeezeos.version ${{DEPLOY_DIR_IMAGE}}/squeezeos.version
}}'''

content = content.replace(old_func, new_func)

with open(class_path, 'w') as f:
    f.write(content)

print("Patch applied successfully.")
