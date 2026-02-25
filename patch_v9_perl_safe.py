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
        
        with sftp.file(bb_file, 'r') as f:
            content = f.read().decode()
            
        target = "    mv config.sh.new config.sh\n}"
        # We use double backslashes for the patch literal, which becomes single in the file
        replacement = """    mv config.sh.new config.sh
    # Inject math and real-time libraries for miniperl linking
    sed -i -e "s|libs='|libs='-lm -lrt |" config.sh
    sed -i -e "s|perllibs='|perllibs='-lm -lrt |" config.sh
    # Re-generate Makefile and config.h from patched config.sh
    sh ./config.sh
}"""

        if target in content:
            new_content = content.replace(target, replacement)
            with sftp.file(bb_file, 'w') as f:
                f.write(new_content)
            print("Successfully applied safe patch to perl-native")
        else:
            print("Target string not found - check file structure!")
            
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
