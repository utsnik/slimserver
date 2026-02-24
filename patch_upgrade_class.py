import sys
import os

class_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/classes/squeezeos-upgrade-image.bbclass'
if not os.path.exists(class_path):
    print(f"Error: {class_path} not found")
    sys.exit(1)

with open(class_path, 'r') as f:
    lines = f.readlines()

new_lines = []
skip_shell_func = False
for line in lines:
    if 'squeezeos_version() {' in line:
        skip_shell_func = True
        continue
    if skip_shell_func:
        if line.strip() == '}':
            skip_shell_func = False
        continue
    new_lines.append(line)

# Add the combined python version definition
python_func = """
python squeezeos_version() {
    import os, bb, datetime
    
    staging = bb.data.getVar('STAGING_DIR_TARGET', d, 1)
    rootfs = bb.data.getVar('IMAGE_ROOTFS', d, 1)
    distro_release = bb.data.getVar('DISTRO_RELEASE', d, 1)
    metadata_revision = bb.data.getVar('METADATA_REVISION', d, 1)
    
    try:
        rev_file = os.path.join(staging, 'squeezeos_squeezeplay_revision')
        revision = open(rev_file, 'r').readline().strip()
    except:
        revision = "unknown"
        
    version_str = f"{distro_release} r{revision}"
    
    os.makedirs(os.path.join(rootfs, 'etc'), exist_ok=True)
    with open(os.path.join(rootfs, 'etc', 'squeezeos.version'), 'w') as f:
        f.write(f"{version_str}\\n")
        f.write(f"build@builder {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write(f"Base build revision: {metadata_revision}\\n")
}
"""

final_content = "".join(new_lines) + python_func

with open(class_path, 'w') as f:
    f.write(final_content)

print("Successfully converted squeezeos_version to a python function")
