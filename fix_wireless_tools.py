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
        bb_file = '/home/utking/squeezeos-build/src/poky/meta/packages/wireless-tools/wireless-tools_29.bb'
        
        try:
            with sftp.file(bb_file, 'r') as f:
                content = f.read().decode()
                
            # HP Labs took down their ancient 1990s website. Route the SRC_URI to an Ubuntu mirror.
            patched_content = re.sub(
                r'http://www\.hpl\.hp\.com/personal/Jean_Tourrilhes/Linux/wireless_tools\.\$\{PV\}\.tar\.gz',
                r'http://archive.ubuntu.com/ubuntu/pool/main/w/wireless-tools/wireless-tools_${PV}.orig.tar.gz',
                content
            )
            
            if patched_content != content:
                with sftp.file(bb_file, 'w') as f:
                    f.write(patched_content)
                print(f"Patched HP mirror to Ubuntu Archive inside {bb_file}")
            else:
                print("No patch needed or pattern not found.")
                
        except Exception as e:
            print(f"Error accessing recipe: {e}")

        sftp.close()
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
