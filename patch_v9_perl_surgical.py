import paramiko
import re

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        sftp = client.open_sftp()
        bb_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/perl/perl-native_5.10.0.bb'
        
        with sftp.file(bb_file, 'r') as f:
            content = f.read().decode()
            
        do_configure_fix = """do_configure () {
    ./Configure \\
        -Dcc="${CC}" \\
        -Dcflags="${CFLAGS}" \\
        -Dldflags="${LDFLAGS}" \\
        -Dcf_by="Open Embedded" \\
        -Dprefix=${prefix} \\
        -Dvendorprefix=${prefix} \\
        -Dvendorprefix=${prefix} \\
        -Dsiteprefix=${prefix} \\
        \\
        -Dprivlib=${STAGING_LIBDIR}/perl/${PV} \\
        -Darchlib=${STAGING_LIBDIR}/perl/${PV} \\
        -Dvendorlib=${STAGING_LIBDIR}/perl/${PV} \\
        -Dvendorarch=${STAGING_LIBDIR}/perl/${PV} \\
        -Dsitelib=${STAGING_LIBDIR}/perl/${PV} \\
        -Dsitearch=${STAGING_LIBDIR}/perl/${PV} \\
        \\
        -Uuseshrplib \\
        -Uusethreads \\
        -Uuseithreads \\
        -Uuselargefiles \\
        -Ud_dosuid \\
        -Ui_db \\
        -Ui_ndbm \\
        -Ui_gdbm \\
        -Di_shadow \\
        -Di_syslog \\
        -Duseperlio \\
        -Dman3ext=3pm \\
        -Uafs \\
        -Ud_csh \\
        -Uusesfio \\
        -Uusenm -des
    # Inject math and real-time libraries for miniperl linking
    sed -i -e "s|libs='|libs='-lm -lrt |" config.sh
    sed -i -e "s|perllibs='|perllibs='-lm -lrt |" config.sh
    # Re-generate Makefile and config.h from patched config.sh
    sh ./config.sh
    sed 's!${STAGING_DIR}/bin!${STAGING_BINDIR}!;
         s!${STAGING_DIR}/lib!${STAGING_LIBDIR}!' < config.sh > config.sh.new
    mv config.sh.new config.sh
}"""

        # Replace the entire do_configure block
        new_content = re.sub(r'do_configure \(\) \{.*?\}', do_configure_fix, content, flags=re.DOTALL)
        
        with sftp.file(bb_file, 'w') as f:
            f.write(new_content)
        print(f"Successfully applied correct surgical patch to {bb_file}")
            
        sftp.close()
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
