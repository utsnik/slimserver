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
            
        if '-lm -lrt' not in content:
            # More robust insertion
            # We look for the final mv config.sh.new config.sh which is very stable
            target = "    mv config.sh.new config.sh"
            replacement = """    mv config.sh.new config.sh
    sed -i -e "s|libs='|libs='-lm -lrt |" config.sh
    sed -i -e "s|perllibs='|perllibs='-lm -lrt |" config.sh"""
            
            if target in content:
                content = content.replace(target, replacement)
                with sftp.file(bb_file, 'w') as f:
                    f.write(content)
                print(f"Successfully patched {bb_file} with math libraries")
            else:
                print(f"Target string not found in {bb_file}")
        else:
            print("Perl native recipe already patched.")
            
        sftp.close()
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
