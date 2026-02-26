import paramiko

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
        
        try:
            with sftp.file(bb_file, 'r') as f:
                content = f.read().decode()
        except FileNotFoundError:
            bb_file = '/home/utking/squeezeos-build/src/poky/meta/packages/perl/perl-native_5.10.0.bb'
            with sftp.file(bb_file, 'r') as f:
                content = f.read().decode()
                
        if '-lm -lrt' not in content:
            # Inject math library linking fix before the final config.sh move
            fix = """	sed -i -e "s|\\(perllibs=.*\\)|\\1 -lm -lrt|" config.sh
	sed -i -e "s|\\(libs=.*\\)|\\1 -lm -lrt|" config.sh
	sed 's!${STAGING_DIR}/bin!${STAGING_BINDIR}!;"""
            content = content.replace("sed 's!${STAGING_DIR}/bin!${STAGING_BINDIR}!;", fix)
            
            with sftp.file(bb_file, 'w') as f:
                f.write(content)
            print(f"Successfully patched {bb_file} with math libraries using robust anchor")
        else:
            print("Perl native recipe already patched.")
            
        sftp.close()
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
