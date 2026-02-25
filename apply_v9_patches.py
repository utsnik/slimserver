import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        # 1. Patch GCC flags
        tune_file = '/home/utking/squeezeos-build/src/poky/meta/conf/machine/include/tune-arm926ejs.inc'
        sftp = client.open_sftp()
        with sftp.file(tune_file, 'r') as f:
            tune_content = f.read().decode()
        
        if 'TARGET_CC_ARCH = "-march=armv5te -mtune=arm926ej-s -O2 -pipe -fomit-frame-pointer"' not in tune_content:
            tune_content = tune_content.replace('TARGET_CC_ARCH = "-march=armv5te -mtune=arm926ej-s"', 'TARGET_CC_ARCH = "-march=armv5te -mtune=arm926ej-s -O2 -pipe -fomit-frame-pointer"')
            with sftp.file(tune_file, 'w') as f:
                f.write(tune_content)
            print("Patched tune-arm926ejs.inc with -O2")
        else:
            print("tune-arm926ejs.inc already patched")
        
        # 2. Add sysctl config via a base-files bbappend
        bbappend_dir = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/base-files/'
        client.exec_command(f'mkdir -p {bbappend_dir}')
        bbappend_file = bbappend_dir + 'base-files_3.0.14.bbappend'
        
        bbappend_content = """do_install_append () {
    echo "vm.swappiness = 10" >> ${D}${sysconfdir}/sysctl.conf
    echo "vm.dirty_ratio = 60" >> ${D}${sysconfdir}/sysctl.conf
}
"""
        with sftp.file(bbappend_file, 'w') as f:
            f.write(bbappend_content)
        print("Created base-files_3.0.14.bbappend for kernel tuning")
        
        # 3. Apply the Lua Snappiness patch
        stdin, stdout, stderr = client.exec_command('cd /home/utking/squeezeos-build/ && patch -p1 < src/radio_snappiness_full.patch')
        out = stdout.read().decode()
        err = stderr.read().decode()
        print("Patch output:", out)
        print("Patch error:", err)
        
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
