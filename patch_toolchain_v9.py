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
        
        files_to_patch = [
            '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/meta/external-csl-toolchain_2010q1-202-modified.bb',
            '/home/utking/squeezeos-build/src/poky/meta/packages/meta/external-csl-toolchain_2010q1-202.bb'
        ]
        
        for file_path in files_to_patch:
            try:
                with sftp.file(file_path, 'r') as f:
                    content = f.read().decode()
                
                if 'sourcery.sw.siemens.com' in content:
                    content = content.replace('https://sourcery.sw.siemens.com/public/gnu_toolchain/', 'http://sourcery.mentor.com/public/gnu_toolchain/')
                    with sftp.file(file_path, 'w') as f:
                        f.write(content)
                    print(f"Patched {file_path}")
                else:
                    print(f"Skipped {file_path} (URL already patched or not found)")
            except Exception as e:
                print(f"Could not patch {file_path}: {e}")
                
        sftp.close()
        client.close()
        
        print("Done pitching toolchain URIs.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
