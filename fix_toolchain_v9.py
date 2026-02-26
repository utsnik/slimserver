import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        # We need to manually download the toolchain to the sources directory to bypass the dead URL
        sources_dir = '/home/utking/squeezeos-build/src/poky/sources'
        toolchain_file = 'arm-2010q1-202-arm-none-linux-gnueabi-i686-pc-linux-gnu.tar.bz2'
        toolchain_url = 'https://raw.githubusercontent.com/ralph-irving/squeezeos-squeezeplay/master/arm-2010q1-202-arm-none-linux-gnueabi-i686-pc-linux-gnu.tar.bz2' # We need a reliable source, I will use a known good URL or search for one.
        
        # Let's check if we already have it in the old 7.8.0 build tree? It should be in the shared sources!
        # Ah, the sources directory is shared between builds. Let's see if it's there.
        stdin, stdout, stderr = client.exec_command(f"ls -l {sources_dir}/{toolchain_file}")
        out = stdout.read().decode()
        if toolchain_file in out:
            print(f"Toolchain already exists in {sources_dir}")
        else:
            print(f"Toolchain not found in {sources_dir}. Need to fetch it.")
            # Let's search the whole server for it
            stdin, stdout, stderr = client.exec_command(f"find /home/utking -name {toolchain_file}")
            found_paths = stdout.read().decode().strip().split('\n')
            if found_paths and found_paths[0]:
                print(f"Found it at: {found_paths[0]}, copying...")
                client.exec_command(f"cp {found_paths[0]} {sources_dir}/")
            else:
                 print("Could not find the toolchain file anywhere on the server.")
        
        # To bypass the URL check entirely, we can set PREMIRRORS or just create a file:// URI.
        # Let's patch the recipe again to use file:// since we have it locally.
        bb_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/meta/external-csl-toolchain_2010q1-202-modified.bb'
        bb_base = '/home/utking/squeezeos-build/src/poky/meta/packages/meta/external-csl-toolchain_2010q1-202.bb'
        
        sftp = client.open_sftp()
        for fpath in [bb_file, bb_base]:
            try:
                with sftp.file(fpath, 'r') as f:
                    content = f.read().decode()
                
                # Replace any remote URL with the local file:// URI
                import re
                content = re.sub(r'(https?|ftp)://[^ \n]+(arm-2010q1-202-arm-none-linux-gnueabi-i686-pc-linux-gnu\.tar\.bz2)', 
                                 r'file:///home/squeezeos/poky/sources/\2', content)
                
                with sftp.file(fpath, 'w') as f:
                    f.write(content)
                print(f"Patched {fpath} to use local file:// URI")
            except Exception as e:
                print(f"Error patching {fpath}: {e}")

        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
