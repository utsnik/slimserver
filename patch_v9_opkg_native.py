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
        bb_file = '/home/utking/squeezeos-build/src/poky/meta/packages/opkg/opkg-native_svn.bb'
        
        with sftp.file(bb_file, 'r') as f:
            content = f.read().decode()
            
        line_to_add = '\nEXTRA_OECONF += "--disable-werror"\nBUILD_CFLAGS += "-Wno-error"\n'
        
        if 'BUILD_CFLAGS += "-Wno-error"' not in content:
            new_content = content + line_to_add
            with sftp.file(bb_file, 'w') as f:
                f.write(new_content)
            print("Successfully patched opkg-native_svn.bb to disable Werror")
        else:
            print("Already patched or BUILD_CFLAGS already set")
            
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
