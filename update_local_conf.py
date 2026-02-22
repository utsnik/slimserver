import os

conf_path = '/home/utking/squeezeos-build/src/build/conf/local.conf'

if not os.path.exists(conf_path):
    print(f"Error: {conf_path} not found")
    exit(1)

overrides = [
    '\n# Direct fetch from GitHub to bypass broken local file protocol\n',
    'SQUEEZEOS_SVN = "git://github.com/ralph-irving/squeezeos.git;branch=public/7.8;protocol=https"\n',
    'SQUEEZEPLAY_SCM = "git://github.com/ralph-irving/squeezeos-squeezeplay.git;branch=public/7.8;protocol=https"\n'
]

with open(conf_path, 'a') as f:
    f.writelines(overrides)

print("Successfully appended GitHub overrides to local.conf")
