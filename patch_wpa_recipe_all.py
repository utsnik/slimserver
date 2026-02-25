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
        bb_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/wpa-supplicant/wpa-supplicant_2.10.bb'
        
        try:
            with sftp.file(bb_file, 'r') as f:
                content = f.read().decode()
                
            # Filter out all file://*.patch lines from the recipe to ignore these broken Yocto upstream patches
            # We keep defconfig, wifi_interface_up_baby, and wifi_disconnect_baby.
            patched_content = re.sub(r'^\s*file://.*\.patch;patch=1;pnum=0\s*\\\s*\n', '', content, flags=re.MULTILINE)
            
            if patched_content != content:
                with sftp.file(bb_file, 'w') as f:
                    f.write(patched_content)
                print(f"Stripped all modern .patch lines from {bb_file}")
            else:
                print("No patches found to strip. Already clean.")
                
        except Exception as e:
            print(f"Error accessing recipe: {e}")

        sftp.close()
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
