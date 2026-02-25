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
        bb_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/alsa/alsa-utils_1.0.18.bb'
        
        with sftp.file(bb_file, 'r') as f:
            content = f.read().decode()
            
        old_sed = 'sed -i -e s:/usr/include/ncurses:${STAGING_INCDIR}/ncurses:g $i'
        new_sed = old_sed + '\n\t\tsed -i -e "s/-ltinfo//g" $i'
        
        if old_sed in content and 's/-ltinfo//g' not in content:
            new_content = content.replace(old_sed, new_sed)
            with sftp.file(bb_file, 'w') as f:
                f.write(new_content)
            print("Successfully patched alsa-utils_1.0.18.bb to remove -ltinfo")
        else:
            print("Target sed not found or already patched")
            
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
